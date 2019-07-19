import datetime
import logging
import os
import sys
import time
import uuid

from flask import Flask
from flask import abort, render_template, redirect, request, Response, url_for
from flask_sqlalchemy import SQLAlchemy

import google.cloud.logging

import requests

from subreddits import SUBREDDIT_INFO


RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET = os.environ.get('RECAPTCHA_SECRET_KEY')


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


class Account(db.Model):
    email = db.Column(db.String(320), primary_key=True)
    uuid = db.Column(
        db.String(36),
        unique=True,
        default=lambda: str(uuid.uuid4()),
    )
    active = db.Column(db.Boolean, default=True, nullable=False)
    last_email = db.Column(db.DateTime)
    signup_time = db.Column(db.DateTime,
                            server_default=db.func.now(),
                            nullable=False)

    def __repr__(self):
        return f'<Account {self.email}>'


class Subreddit(db.Model):
    name = db.Column(db.String(21), primary_key=True)

    def __repr__(self):
        return f'<Subreddit {self.name}>'


class SubredditPost(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    subreddit_name = db.Column(db.String(21),
                               db.ForeignKey('subreddit.name'),
                               nullable=False)
    subreddit = db.relationship('Subreddit')
    title = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(2000), nullable=False)

    scraped_at = db.Column(db.DateTime,
                           server_default=db.func.now(),
                           nullable=False)
    preview_image_url = db.Column(db.String(2000))
    permalink_url = db.Column(db.String(2000))
    num_comments = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<SubredditPost {self.id}>'


class EmailEventSubreddit(db.Model):
    """
    The relationship between email events and subreddits, with search terms.
    """
    email_event_id = db.Column(db.Integer, db.ForeignKey(
        "email_event.id", ondelete="cascade"), primary_key=True)
    subreddit_name = db.Column(db.String(21), db.ForeignKey(
        "subreddit.name"), primary_key=True)
    search_term = db.Column(db.String(512), primary_key=True)

    email_event = db.relationship(
        'EmailEvent', backref='email_event_subreddits')
    subreddit = db.relationship('Subreddit')

    def __repr__(self):
        return (
            f'<EmailEventSubreddit '
            f'{self.email_event_id} {self.subreddit_name} {self.search_term}>')


class EmailEvent(db.Model):
    """
    Recurring event model for emails to be sent to accounts.
    """
    id = db.Column(db.Integer, primary_key=True)
    account_email = db.Column(
        db.String(320),
        db.ForeignKey('account.email', onupdate='cascade'),
        nullable=False,
    )
    account = db.relationship('Account', backref='email_events')
    time_of_day = db.Column(db.Time, nullable=False)
    day_of_week = db.Column(db.Integer)

    def __repr__(self):
        return f'<EmailEvent {self.id}>'


class ScrapeRecordSubredditPost(db.Model):
    """
    The relationship between scrape_records and subreddit_posts
    """
    scrape_record_id = db.Column(db.Integer,
                                 db.ForeignKey('scrape_record.id'),
                                 primary_key=True)
    subreddit_post_id = db.Column(db.String(128),
                                  db.ForeignKey('subreddit_post.id'),
                                  primary_key=True)
    ordinal = db.Column(db.Integer, nullable=False)

    scrape_record = db.relationship('ScrapeRecord')
    subreddit_post = db.relationship('SubredditPost')

    def __repr__(self):
        return (f'<ScrapeRecordSubredditPost '
                f'{self.scrape_record_id} {self.subreddit_post_id}>')


class ScrapeRecord(db.Model):
    """
    A grouping of subreddit posts from a scraping event
    """
    id = db.Column(db.Integer, primary_key=True)
    interval = db.Column(
        db.Enum('daily', 'weekly', name='interval_enum'), nullable=False)
    scrape_time = db.Column(db.DateTime,
                            server_default=db.func.now(),
                            nullable=False)
    subreddit_name = db.Column(
        db.String(21), db.ForeignKey("subreddit.name"), nullable=False)
    search_term = db.Column(db.String(512), nullable=False)

    subreddit = db.relationship('Subreddit')
    scrape_record_subreddit_posts = db.relationship(
        'ScrapeRecordSubredditPost')
    subreddit_posts = db.relationship(
        'SubredditPost',
        backref='scrape_records',
        order_by='ScrapeRecordSubredditPost.ordinal',
        secondary=ScrapeRecordSubredditPost.__table__)

    def __repr__(self):
        return f'<ScrapeRecord {self.id}>'


@app.context_processor
def add_now():
    return {'now': datetime.datetime.utcnow()}


@app.before_request
def https_redirect():
    if (request.headers.get('X-Forwarded-Proto', 'http') != 'https' and
            request.endpoint != 'health_check' and
            not app.config['DEBUG']):
        return redirect(request.url.replace('http://', 'https://', 1),
                        code=301)


@app.route("/")
def index():
    cache_time = time.time() if app.config['DEBUG'] else APP_START_TIME
    return render_template('index.html',
                           cache_timestamp=str(int(cache_time)),
                           subreddit_info=SUBREDDIT_INFO,
                           recaptcha_site_key=RECAPTCHA_SITE_KEY)


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
        subreddits = request.form.getlist('subreddits[]')
        if len(subreddits) > 10:
            return 'too many subreddits', 400
        account.email_events[0].subreddits = Subreddit.query.filter(
            Subreddit.name.in_(subreddits)).all()
        account.email_events[0].day_of_week = (
            6 if request.form['email_interval'] == 'weekly' else None)
        db.session.commit()
    return render_template(
        'manage.html',
        account=account,
        email_interval=(
            'weekly' if account.email_events[0].day_of_week else 'daily'),
        user_subreddits=[s.name for s in account.email_events[0].subreddits],
        subreddit_info=SUBREDDIT_INFO,
    )


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
    if not app.config['DEBUG']:
        _check_captcha(request.form['captcha_token'])
    email = request.form['email'].lower()
    if Account.query.get(email) is not None:
        return 'account already exists', 400
    subreddits = request.form.getlist('subreddits[]')
    if len(subreddits) > 10:
        return 'too many subreddits', 400
    subreddits = Subreddit.query.filter(Subreddit.name.in_(subreddits)).all()
    email_interval = request.form['email_interval']
    db.session.add(Account(
        email=email,
        email_events=[EmailEvent(
            account_email=email,
            time_of_day=datetime.time(12),
            day_of_week=6 if email_interval == 'weekly' else None,
            subreddits=subreddits,
        )]
    ))
    db.session.commit()
    return 'success', 201


def _check_captcha(token):
    logging.info(f'Checking captcha token: {token}')
    resp = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': RECAPTCHA_SECRET,
            'response': token,
        })
    try:
        resp.raise_for_status()
        data = resp.json()
        logging.info(f'Response: {data}')
        if not data['success']:
            abort(Response('Could not verify captcha', status=400))
    except Exception:
        logging.exception('Error verifying captcha')
        abort(Response('Could not verify captcha', status=400))
