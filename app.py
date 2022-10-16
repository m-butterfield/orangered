import datetime
import logging
import os
import sys
from typing import Dict, List, Tuple, TYPE_CHECKING, Union

from flask import Flask
from flask import abort, render_template, redirect, request, Response, url_for

from subreddits import SUBREDDITS

if TYPE_CHECKING:
    from werkzeug import Response


RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET = os.environ.get("RECAPTCHA_SECRET_KEY")


class Config:
    SERVER_NAME = os.environ.get("SERVER_NAME")
    APP_BASE_URL = os.environ.get("APP_BASE_URL", "http://localhost:8000")
    PREFERRED_URL_SCHEME = "https" if SERVER_NAME == "app.orangered.email" else "http"


app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger("parso").setLevel(logging.WARNING)


if os.getenv("RENDER_STATIC"):

    @app.route("/")
    def index() -> str:
        return render_template(
            "index.html",
            recaptcha_site_key=RECAPTCHA_SITE_KEY,
            subreddits=SUBREDDITS,
            app_base_url=app.config["APP_BASE_URL"],
        )

    @app.route("/manage")
    def manage() -> str:
        return render_template(
            "manage.html",
            subreddits=SUBREDDITS,
            app_base_url=app.config["APP_BASE_URL"],
        )

    @app.route("/unsubscribe")
    def unsubscribe() -> str:
        return render_template(
            "unsubscribe.html", app_base_url=app.config["APP_BASE_URL"]
        )


@app.route("/account/<account_uuid>", methods=["GET", "POST"])
def account(account_uuid: str) -> Union[Dict, Tuple[str, int], "Response"]:
    from db import Account, Session, Subreddit

    with Session() as session:
        account = (
            session.query(Account).filter(Account.uuid == account_uuid).one_or_none()
        )
        if account is None:
            return "not found", 404
        if request.method == "POST":
            data: Dict[str, Union[str, List[str]]] = request.json or {}
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
        return _serialize_account(account)


@app.route("/unsubscribe/<account_uuid>", methods=["POST"])
def unsubscribe_account(account_uuid) -> Tuple[str, int]:
    from db import Account, Session

    with Session() as session:
        account = (
            session.query(Account).filter(Account.uuid == account_uuid).one_or_none()
        )
        if account is None:
            return "account not found", 404
        data = request.get_json()
        account.active = not data["unsubscribe"]
        session.commit()
        return "success", 200


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
    from sendgrid import From, Mail, SendGridAPIClient

    with Session() as session:
        data = request.get_json()
        if not app.config["DEBUG"]:
            _check_captcha(data["captchaToken"])
        email = data["email"].lower()
        if session.query(Account).get(email) is not None:
            return "account already exists", 400
        subs = data["subreddits"]
        if len(subs) > 10:
            return "too many subreddits", 400
        subreddits = session.query(Subreddit).filter(Subreddit.name.in_(subs)).all()
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
        if not app.config["DEBUG"]:
            SendGridAPIClient(os.environ.get("SENDGRID_API_KEY")).send(
                Mail(
                    from_email=From("postman@orangered.email", "Orangered"),
                    to_emails="matt@mattbutterfield.com",
                    subject="New Orangered Signup",
                    plain_text_content=f"You have a new signup: {email}, with subreddits: {', '.join(subs)}",
                )
            )
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
