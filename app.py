from datetime import datetime
import os
import time
import uuid

from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, DateTime, ForeignKey, func, String
from sqlalchemy.orm import relationship


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


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

APP_START_TIME = time.time()


@app.before_request
def https_redirect():
    if (not request.headers.get('X-Forwarded-Proto', 'http') == 'https' and not
            app.config['DEBUG']):
        return redirect(request.url.replace('http://', 'https://', 1),
                        code=301)


account_subreddit = db.Table(
    "account_subreddit", db.Model.metadata,
    Column("account_email", String(255), ForeignKey(
        "account.email", onupdate="cascade"),
           primary_key=True),
    Column("subreddit_name", String(255), ForeignKey("subreddit.name"),
           primary_key=True),
)


class Account(db.Model):
    email = Column(String(255), primary_key=True)
    uuid = Column(String(80), unique=True, default=lambda: str(uuid.uuid4()))
    subreddits = relationship('Subreddit',
                              backref='accounts', secondary=account_subreddit)

    def __repr__(self):
        return f'<Account {self.email}>'


class Subreddit(db.Model):
    name = Column(String(255), primary_key=True)
    last_scraped = Column(DateTime())

    def __repr__(self):
        return f'<Subreddit {self.name}>'


class SubredditPost(db.Model):
    id = Column(String(128), primary_key=True)
    subreddit_name = Column(String(255), ForeignKey('subreddit.name'),
                            nullable=False)
    subreddit = relationship('Subreddit')
    title = Column(String(512), nullable=False)
    url = Column(String(255), nullable=False)

    scraped_at = Column(DateTime(), default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<SubredditPost {self.id}>'


@app.route("/")
def index():
    subreddit_names = [s.name for s in db.session.query(
        Subreddit).order_by(func.lower(Subreddit.name))]
    cache_time = time.time() if app.config['DEBUG'] else APP_START_TIME
    return render_template('index.html',
                           cache_timestamp=str(int(cache_time)),
                           subreddits=subreddit_names)


@app.route("/signup", methods=['POST'])
def signup():
    email = request.form['email']
    subreddits = db.session.query(Subreddit).filter(Subreddit.name.in_(
        request.form.getlist('subreddits[]'))).all()
    db.session.add(Account(
        email=email,
        subreddits=subreddits,
    ))
    db.session.commit()
    return 'success', 201
