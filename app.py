import datetime
import logging
import os
import sys

from flask import Flask
from flask import abort, render_template, redirect, request, Response, url_for


from subreddits import SUBREDDITS


RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET = os.environ.get("RECAPTCHA_SECRET_KEY")


class Config:
    SERVER_NAME = os.environ.get("SERVER_NAME")
    PREFERRED_URL_SCHEME = "https" if SERVER_NAME == "orangered.email" else "http"


app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger("parso").setLevel(logging.WARNING)


@app.route("/")
def index():
    return render_template(
        "index.html",
        recaptcha_site_key=RECAPTCHA_SITE_KEY,
        subreddits=SUBREDDITS,
    )


@app.route("/account/<account_uuid>/manage", methods=["GET", "POST"])
def manage(account_uuid):
    from db import Account, Session, Subreddit

    with Session() as session:
        account = (
            session.query(Account).filter(Account.uuid == account_uuid).one_or_none()
        )
        if account is None:
            return "not found", 404
        if not account.active:
            return redirect(url_for("unsubscribe", account_uuid=account_uuid))
        if request.method == "POST":
            data = request.get_json()
            subreddits = data["subreddits"]
            if len(subreddits) > 10:
                return "too many subreddits", 400
            account.email_events[0].subreddits = (
                session.query(Subreddit).filter(Subreddit.name.in_(subreddits)).all()
            )
            account.email_events[0].day_of_week = (
                6 if data["emailInterval"] == "weekly" else None
            )
            session.commit()
            return "success", 200
        return render_template(
            "manage.html",
            account_info=_serialize_account(account),
            subreddits=SUBREDDITS,
        )


@app.route("/account/<account_uuid>/unsubscribe", methods=["GET", "POST"])
def unsubscribe(account_uuid):
    from db import Account, Session

    with Session() as session:
        account = (
            session.query(Account).filter(Account.uuid == account_uuid).one_or_none()
        )
        if account is None:
            return "account not found", 404
        if request.method == "POST":
            data = request.get_json()
            account.active = not data["unsubscribe"]
            session.commit()
        return render_template(
            "unsubscribe.html", account_info=_serialize_account(account)
        )


def _serialize_account(account):
    return {
        "id": account.uuid,
        "active": account.active,
        "email": account.email,
        "subreddits": [s.name for s in account.email_events[0].subreddits],
        "emailInterval": ("weekly" if account.email_events[0].day_of_week else "daily"),
    }


@app.route("/signup", methods=["POST"])
def signup():
    from db import Account, EmailEvent, Session, Subreddit

    with Session() as session:
        data = request.get_json()
        if not app.config["DEBUG"]:
            _check_captcha(data["captchaToken"])
        email = data["email"].lower()
        if session.query(Account).get(email) is not None:
            return "account already exists", 400
        subreddits = data["subreddits"]
        if len(subreddits) > 10:
            return "too many subreddits", 400
        subreddits = (
            session.query(Subreddit).filter(Subreddit.name.in_(subreddits)).all()
        )
        email_interval = data["emailInterval"]
        session.add(
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
        session.commit()
        return "success", 201


def _check_captcha(token):
    import requests

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
