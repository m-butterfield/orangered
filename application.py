import os
import time
import uuid

from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, String, ForeignKey, func
from sqlalchemy.orm import relationship


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)

APP_START_TIME = time.time()


user_subreddit = db.Table("user_subreddit", db.Model.metadata,
    Column("user_email", String, ForeignKey("user.email"), primary_key=True),
    Column("subreddit_name", String, ForeignKey("subreddit.name"), primary_key=True),
)


class User(db.Model):
    email = Column(String(255), primary_key=True)
    uuid = Column(String(80), unique=True, default=lambda: str(uuid.uuid4()))
    subreddits = relationship('Subreddit', secondary=user_subreddit)

    def __repr__(self):
        return '<User %r>' % self.email


class Subreddit(db.Model):
    name = Column(String(255), primary_key=True)

    def __repr__(self):
        return '<Subreddit %r>' % self.name


@application.route("/")
def index():
    subreddit_names = [s.name for s in db.session.query(
        Subreddit).order_by(func.lower(Subreddit.name))]
    cache_time = time.time() if application.config['DEBUG'] else APP_START_TIME
    return render_template('index.html',
                           cache_timestamp=str(int(cache_time)),
                           subreddits=subreddit_names)


@application.route("/signup", methods=['POST'])
def signup():
    email = request.form['email']
    subreddits = db.session.query(Subreddit).filter(Subreddit.name.in_(
        request.form.getlist('subreddits'))).all()
    db.session.add(User(
        email=email,
        subreddits=subreddits,
    ))
    db.session.commit()
    return 'success', 201
