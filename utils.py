import datetime
import os

from jinja2 import Template

import praw

from application import db, Subreddit, SubredditPost


REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = os.environ.get('REDDIT_USERNAME')
REDDIT_PASSWORD = os.environ.get('REDDIT_PASSWORD')


def send_emails():
    subreddits = _scrape_posts()
    html_template = _template_data()
    data = Template(html_template).render(
            email_management_url='',
            subreddits=subreddits,
    )


def _scrape_posts():
    reddit = _reddit()
    subreddits = []
    for subreddit in db.session.query(Subreddit).join(Subreddit.accounts):
        posts = []
        for result in reddit.subreddit(subreddit.name).top('day', limit=10):
            posts.append(SubredditPost(
                id=result.id,
                url=result.url,
                title=result.title,
                subreddit=subreddit,
            ))
        subreddit.last_scraped = datetime.datetime.utcnow()
        db.session.add_all(posts)
        db.session.commit()
        subreddits.append({'name': subreddit.name, 'posts': posts})


def _reddit():
    return praw.Reddit(client_id=REDDIT_CLIENT_ID,
                       client_secret=REDDIT_CLIENT_SECRET,
                       username=REDDIT_USERNAME,
                       password=REDDIT_PASSWORD,
                       user_agent='orangered by /u/deneb150')


def _template_data():
    with open('templates/email.html') as fp:
        return fp.read()
