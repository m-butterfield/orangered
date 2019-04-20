from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class User(db.Model):
    email = db.Column(db.String(255), primary_key=True)

    def __repr__(self):
        return '<User %r>' % self.email


class Subreddit(db.Model):
    name = db.Column(db.String(255), primary_key=True)

    def __repr__(self):
        return '<Subreddit %r>' % self.name


@app.route("/")
def index():
    return render_template('index.html', subreddits=[
        'aviation',
        'spacex',
        'python',
        'technology',
        'piano',
    ])
