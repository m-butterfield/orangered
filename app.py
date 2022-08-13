import datetime
import logging
import os
import sys
import time
import uuid

from flask import Flask
from flask import abort, render_template, redirect, request, Response, url_for
from flask_sqlalchemy import SQLAlchemy

import requests

from subreddits import SUBREDDITS


RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET = os.environ.get("RECAPTCHA_SECRET_KEY")


def _psql_uri():
    username = os.environ.get("PGUSER")
    password = os.environ.get("PGPASSWORD")
    if username and password:
        return (
            f"postgresql+psycopg2://{username}:{password}@/"
            f'{os.environ.get("PGDATABASE")}'
            f'?host={os.environ.get("PGHOST")}'
        )
    else:
        return (
            f'postgresql+psycopg2://{os.environ.get("PGHOST")}:5432/'
            f'{os.environ.get("PGDATABASE")}'
        )


class Config:
    SQLALCHEMY_DATABASE_URI = _psql_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SERVER_NAME = os.environ.get("SERVER_NAME")
    PREFERRED_URL_SCHEME = "https" if SERVER_NAME == "orangered.email" else "http"


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

APP_START_TIME = time.time()


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger("parso").setLevel(logging.WARNING)


email_event_subreddit = db.Table(
    "email_event_subreddit",
    db.Model.metadata,
    db.Column(
        "email_event_id",
        db.Integer,
        db.ForeignKey("email_event.id", ondelete="cascade"),
        primary_key=True,
    ),
    db.Column(
        "subreddit_name",
        db.String(21),
        db.ForeignKey("subreddit.name", onupdate="cascade"),
        primary_key=True,
    ),
)


class Account(db.Model):
    email = db.Column(db.String(320), primary_key=True)
    uuid = db.Column(
        db.String(36),
        unique=True,
        default=lambda: str(uuid.uuid4()),
    )
    active = db.Column(db.Boolean, default=True, nullable=False)
    last_email = db.Column(db.DateTime)
    signup_time = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<Account {self.email}>"


class Subreddit(db.Model):
    name = db.Column(db.String(21), primary_key=True)

    def __repr__(self):
        return f"<Subreddit {self.name}>"


class SubredditPost(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    subreddit_name = db.Column(
        db.String(21),
        db.ForeignKey("subreddit.name", onupdate="cascade"),
        nullable=False,
    )
    subreddit = db.relationship("Subreddit")
    title = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(2000), nullable=False)

    scraped_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    preview_image_url = db.Column(db.String(2000))
    permalink_url = db.Column(db.String(2000))
    num_comments = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<SubredditPost {self.id}>"


class EmailEvent(db.Model):
    """
    Recurring event model for emails to be sent to accounts.
    """

    id = db.Column(db.Integer, primary_key=True)
    account_email = db.Column(
        db.String(320),
        db.ForeignKey("account.email", onupdate="cascade"),
        nullable=False,
    )
    account = db.relationship("Account", backref="email_events")
    time_of_day = db.Column(db.Time, nullable=False)
    day_of_week = db.Column(db.Integer)

    subreddits = db.relationship(
        "Subreddit",
        backref="email_events",
        order_by="Subreddit.name",
        secondary=email_event_subreddit,
    )


class ScrapeRecordSubredditPost(db.Model):
    """
    The relationship between scrape_records and subreddit_posts
    """

    scrape_record_id = db.Column(
        db.Integer, db.ForeignKey("scrape_record.id"), primary_key=True
    )
    subreddit_post_id = db.Column(
        db.String(128), db.ForeignKey("subreddit_post.id"), primary_key=True
    )
    ordinal = db.Column(db.Integer, nullable=False)

    scrape_record = db.relationship("ScrapeRecord")
    subreddit_post = db.relationship("SubredditPost")


class ScrapeRecord(db.Model):
    """
    A grouping of subreddit posts from a scraping event
    """

    id = db.Column(db.Integer, primary_key=True)
    interval = db.Column(
        db.Enum("daily", "weekly", name="interval_enum"), nullable=False
    )
    scrape_time = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    subreddit_name = db.Column(
        db.String(21), db.ForeignKey("subreddit.name", onupdate="cascade")
    )

    subreddit = db.relationship("Subreddit")
    scrape_record_subreddit_posts = db.relationship("ScrapeRecordSubredditPost")
    subreddit_posts = db.relationship(
        "SubredditPost",
        backref="scrape_records",
        order_by="ScrapeRecordSubredditPost.ordinal",
        secondary=ScrapeRecordSubredditPost.__table__,
    )


@app.context_processor
def add_now():
    return {"now": datetime.datetime.utcnow()}


@app.route("/")
def index():
    return render_template(
        "index.html",
        recaptcha_site_key=RECAPTCHA_SITE_KEY,
        subreddits=SUBREDDITS,
    )


@app.route("/health_check")
def health_check():
    try:
        db.session.execute("SELECT 1")
    except Exception:
        logging.exception("could not connect to database")
        return "could not connect to database", 500
    return "all good"


@app.route("/account/<account_uuid>/manage", methods=["GET", "POST"])
def manage(account_uuid):
    account = Account.query.filter(Account.uuid == account_uuid).one_or_none()
    if account is None:
        return "not found", 404
    if not account.active:
        return redirect(url_for("unsubscribe", account_uuid=account_uuid))
    if request.method == "POST":
        data = request.get_json()
        subreddits = data["subreddits"]
        if len(subreddits) > 10:
            return "too many subreddits", 400
        account.email_events[0].subreddits = Subreddit.query.filter(
            Subreddit.name.in_(subreddits)
        ).all()
        account.email_events[0].day_of_week = (
            6 if data["emailInterval"] == "weekly" else None
        )
        db.session.commit()
        return "success", 200
    return render_template(
        "manage.html",
        account_info={
            "id": account.uuid,
            "active": account.active,
            "email": account.email,
            "subreddits": [s.name for s in account.email_events[0].subreddits],
            "emailInterval": ("weekly" if account.email_events[0].day_of_week else "daily"),
        },
        subreddits=SUBREDDITS,
    )


@app.route("/account/<account_uuid>/unsubscribe", methods=["GET", "POST"])
def unsubscribe(account_uuid):
    account = Account.query.filter(Account.uuid == account_uuid).one_or_none()
    if account is None:
        return "not found", 404
    if request.method == "POST":
        data = request.get_json()
        account.active = data["unsubscribe"] == "False"
        db.session.commit()
    return render_template("unsubscribe.html", account=account)


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not app.config["DEBUG"]:
        _check_captcha(data["captchaToken"])
    email = data["email"].lower()
    if Account.query.get(email) is not None:
        return "account already exists", 400
    subreddits = data["subreddits"]
    if len(subreddits) > 10:
        return "too many subreddits", 400
    subreddits = Subreddit.query.filter(Subreddit.name.in_(subreddits)).all()
    email_interval = data["emailInterval"]
    db.session.add(
        Account(
            email=email,
            email_events=[
                EmailEvent(
                    account_email=email,
                    time_of_day=datetime.time(12),
                    day_of_week=6 if email_interval == "weekly" else None,
                    subreddits=subreddits,
                )
            ],
        )
    )
    db.session.commit()
    return "success", 201


def _check_captcha(token):
    logging.info(f"Checking captcha token: {token}")
    resp = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": RECAPTCHA_SECRET,
            "response": token,
        },
    )
    try:
        resp.raise_for_status()
        data = resp.json()
        logging.info(f"Response: {data}")
        if not data["success"]:
            abort(Response("Could not verify captcha", status=400))
    except Exception:
        logging.exception("Error verifying captcha")
        abort(Response("Could not verify captcha", status=400))
