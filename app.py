from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, String, ForeignKey, func
from sqlalchemy.orm import relationship


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


user_subreddit = db.Table("user_subreddit", db.Model.metadata,
    Column("user_email", String, ForeignKey("user.email"), primary_key=True),
    Column("subreddit_name", String, ForeignKey("subreddit.name"), primary_key=True),
)


class User(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    subreddits = relationship('Subreddit', secondary=user_subreddit)

    def __repr__(self):
        return '<User %r>' % self.email


class Subreddit(db.Model):
    name = db.Column(db.String(255), primary_key=True)

    def __repr__(self):
        return '<Subreddit %r>' % self.name


@app.route("/")
def index():
    subreddit_names = [s.name for s in db.session.query(
        Subreddit).order_by(func.lower(Subreddit.name))]
    return render_template('index.html', subreddits=subreddit_names)
