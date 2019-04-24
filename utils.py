import os

from jinja2 import Template

import praw


REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = os.environ.get('REDDIT_USERNAME')
REDDIT_PASSWORD = os.environ.get('REDDIT_PASSWORD')


def send_emails():
    reddit = _reddit()
    subreddits = []
    template_data = _template_data()
    for name in SUBREDDITS:
        posts = []
        for result in reddit.subreddit(name).top('day', limit=10):
            posts.append({
                'title': result.title,
                'url': result.url,
            })
        subreddits.append({'name': name, 'posts': posts})

    with open('scratch.html', 'w') as fp:
        fp.write(Template(template_data).render(
            email_management_url='',
            subreddits=subreddits,
        ))


def _reddit():
    return praw.Reddit(client_id=REDDIT_CLIENT_ID,
                       client_secret=REDDIT_CLIENT_SECRET,
                       username=REDDIT_USERNAME,
                       password=REDDIT_PASSWORD,
                       user_agent='orangered by /u/deneb150')


def _template_data():
    with open('templates/email.html') as fp:
        return fp.read()
