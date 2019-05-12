from datetime import datetime
import logging
import os
import sys
import time
import uuid

from flask import Flask
from flask import render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

import google.cloud.logging


def _psql_uri():
    username = os.environ.get('PGUSER')
    password = os.environ.get('PGPASSWORD')
    if username and password:
        return (f'postgres://{username}:{password}@'
                f'{os.environ.get("PGHOST")}:5432/'
                f'{os.environ.get("PGDATABASE")}')
    else:
        return (f'postgres://{os.environ.get("PGHOST")}:5432/'
                f'{os.environ.get("PGDATABASE")}')


class Config(object):
    SQLALCHEMY_DATABASE_URI = _psql_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SERVER_NAME = os.environ.get('SERVER_NAME')
    PREFERRED_URL_SCHEME = 'https' if SERVER_NAME == 'orangered.io' else 'http'


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

APP_START_TIME = time.time()


if app.config['DEBUG']:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
else:
    client = google.cloud.logging.Client()
    client.setup_logging()


account_subreddit = db.Table(
    "account_subreddit", db.Model.metadata,
    db.Column("account_email", db.String(320), db.ForeignKey(
        "account.email", onupdate="cascade"),
        primary_key=True),
    db.Column("subreddit_name", db.String(21), db.ForeignKey(
        "subreddit.name"),
        primary_key=True),
)


class Account(db.Model):
    email = db.Column(db.String(320), primary_key=True)
    uuid = db.Column(db.String(36),
                     unique=True, default=lambda: str(uuid.uuid4()))
    active = db.Column(db.Boolean, default=True, nullable=False)
    last_email = db.Column(db.DateTime)
    subreddits = db.relationship('Subreddit',
                                 backref='accounts',
                                 secondary=account_subreddit)

    def __repr__(self):
        return f'<Account {self.email}>'


class Subreddit(db.Model):
    name = db.Column(db.String(21), primary_key=True)
    last_scraped = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Subreddit {self.name}>'


class SubredditPost(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    subreddit_name = db.Column(db.String(21), db.ForeignKey('subreddit.name'),
                               nullable=False)
    subreddit = db.relationship('Subreddit')
    title = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(2000), nullable=False)

    scraped_at = db.Column(db.DateTime,
                           default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<SubredditPost {self.id}>'


@app.before_request
def https_redirect():
    if (request.headers.get('X-Forwarded-Proto', 'http') != 'https' and
            request.endpoint != 'health_check' and
            not app.config['DEBUG']):
        return redirect(request.url.replace('http://', 'https://', 1),
                        code=301)


@app.route("/")
def index():
    subreddit_names = [s.name for s in Subreddit.query.order_by(
        db.func.lower(Subreddit.name))]
    cache_time = time.time() if app.config['DEBUG'] else APP_START_TIME
    return render_template('index.html',
                           cache_timestamp=str(int(cache_time)),
                           subreddits=subreddit_names)


@app.route("/health_check")
def health_check():
    try:
        db.session.execute('SELECT 1')
    except Exception:
        logging.exception('could not connect to database')
        return 'could not connect to database', 500
    return 'all good'


@app.route("/account/<uuid>/manage", methods=['GET', 'POST'])
def manage(uuid):
    account = Account.query.filter(Account.uuid == uuid).one_or_none()
    if account is None:
        return 'not found', 404
    if not account.active:
        return redirect(url_for('unsubscribe', uuid=uuid))
    if request.method == 'POST':
        pass
    return render_template('manage.html', account=account)


@app.route("/account/<uuid>/unsubscribe", methods=['GET', 'POST'])
def unsubscribe(uuid):
    account = Account.query.filter(Account.uuid == uuid).one_or_none()
    if account is None:
        return 'not found', 404
    if request.method == 'POST':
        account.active = request.form['unsubscribe'] == 'False'
        db.session.commit()
    return render_template('unsubscribe.html', account=account)


@app.route("/signup", methods=['POST'])
def signup():
    email = request.form['email']
    if Account.query.get(email.lower()) is not None:
        return 'account already exists', 400
    subreddits = Subreddit.query.filter(Subreddit.name.in_(
        request.form.getlist('subreddits[]'))).all()
    db.session.add(Account(
        email=email.lower(),
        subreddits=subreddits,
    ))
    db.session.commit()
    return 'success', 201
