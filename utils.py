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
    subreddits = scrape_posts()
    html_template = _template_data()
    data = Template(html_template).render(
            email_management_url='',
            subreddits=subreddits,
    )
    with open('scratch.html', 'w') as fp:
        fp.write(data)


def scrape_posts():
    reddit = _reddit()
    subreddits = {}
    now = datetime.datetime.utcnow()
    for subreddit in _subreddits_to_scrape():
        posts = []
        if subreddit.last_scraped and (
                subreddit.last_scraped > now - datetime.timedelta(hours=23)):
            posts = db.session.query(SubredditPost).filter(
                SubredditPost.scraped_at > now - datetime.timedelta(hours=23),
            ).all()
        else:
            for result in reddit.subreddit(subreddit.name).top('day', limit=10):
                post = SubredditPost(
                    id=result.id,
                    url=result.url,
                    title=result.title,
                    subreddit=subreddit,
                )
                posts.append(post)
                db.session.add(post)
        subreddit.last_scraped = now
        db.session.commit()
        if posts:
            subreddits[subreddit.name] = posts
    return subreddits


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
