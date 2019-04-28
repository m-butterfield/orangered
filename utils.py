from datetime import datetime, timedelta
import os

from jinja2 import Template

import praw

from application import Account, db, Subreddit, SubredditPost


REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = os.environ.get('REDDIT_USERNAME')
REDDIT_PASSWORD = os.environ.get('REDDIT_PASSWORD')


def send_emails():
    _send_emails(_scrape_posts())


def _send_emails(subreddit_posts):
    html_template = _template_data()
    for account in db.session.query(Account):
        _send_email_for_account(account, subreddit_posts, html_template)


def _send_email_for_account(account, subreddit_posts, html_template):
    subreddits = sorted(
        [(s.name, subreddit_posts[s.name]) for s in account.subreddits],
        key=lambda s: s[0].lower(),
    )
    data = Template(html_template).render(
        email_management_url='',
        subreddits=subreddits,
    )
    # with open('scratch.html', 'w') as fp:
    #     fp.write(data)


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
                       user_agent='orangered by /u/deneb150')


def _template_data():
    with open('templates/email.html') as fp:
        return fp.read()
