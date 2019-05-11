from datetime import datetime, timedelta
import os
import requests

from jinja2 import Template

import praw

from app import Account, db, Subreddit, SubredditPost


MAILGUN_API_URL = "https://api.mailgun.net/v3/orangered.io/messages"
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')


REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = os.environ.get('REDDIT_USERNAME')
REDDIT_PASSWORD = os.environ.get('REDDIT_PASSWORD')


def _html_template():
    with open('templates/email.html') as fp:
        return fp.read()


def _text_template():
    with open('templates/email.txt') as fp:
        return fp.read()


HTML_TEMPLATE, TEXT_TEMPLATE = _html_template(), _text_template()


def send_emails():
    _send_emails(_scrape_posts())


def _send_emails(subreddit_posts):
    for account in db.session.query(Account):
        _send_email_for_account(account, subreddit_posts)


def _send_email_for_account(account, subreddit_posts):
    subreddits = sorted(
        [(s.name, subreddit_posts[s.name]) for s in account.subreddits],
        key=lambda s: s[0].lower(),
    )
    html_data = Template(HTML_TEMPLATE, trim_blocks=True).render(
        email_management_url='',
        subreddits=subreddits,
    )
    text_data = Template(TEXT_TEMPLATE, trim_blocks=True).render(
        email_management_url='',
        subreddits=subreddits,
    )
    _send_email(account.email, html_data, text_data)


def _send_email(email, html, text):
    resp = requests.post(
        MAILGUN_API_URL,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": "Orangered <no-reply@orangered.io>",
            "to": [email],
            "subject": "Orangered - Your daily Reddit summary",
            "html": html,
            "text": text,
        })
    resp.raise_for_status()


def _scrape_posts():
    reddit = _reddit()
    subreddit_posts = {}
    now = datetime.utcnow()
    for subreddit in _subreddits_to_scrape():
        if subreddit.last_scraped and (
                subreddit.last_scraped > now - timedelta(hours=23)):
            posts = _existing_scraped_posts(subreddit, now)
        else:
            posts = _scrape_new_posts(reddit, subreddit)
        subreddit_posts[subreddit.name] = posts
    return subreddit_posts


def _existing_scraped_posts(subreddit, now):
    return db.session.query(SubredditPost).filter(
        SubredditPost.subreddit == subreddit,
        SubredditPost.scraped_at > now - timedelta(hours=23),
    ).all()


def _scrape_new_posts(reddit, subreddit):
    posts = [
        SubredditPost(
            id=result.id,
            url=result.url,
            title=result.title,
            subreddit=subreddit,
        )
        for result in reddit.subreddit(subreddit.name).top('day', limit=10)
    ]
    db.session.add_all(posts)
    subreddit.last_scraped = datetime.utcnow()
    db.session.commit()
    return posts


def _subreddits_to_scrape():
    return db.session.query(Subreddit).join(Subreddit.accounts)


def _reddit():
    return praw.Reddit(client_id=REDDIT_CLIENT_ID,
                       client_secret=REDDIT_CLIENT_SECRET,
                       username=REDDIT_USERNAME,
                       password=REDDIT_PASSWORD,
                       user_agent='orangered')
