from collections import OrderedDict
from datetime import datetime, timedelta
import logging
import os

from flask import url_for

from jinja2 import Template

import praw

import requests

from app import Account, app, db, EmailEvent, Subreddit, SubredditPost

from subreddits import SUBREDDITS


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


def insert_subreddits():
    db.session.add_all([Subreddit(name=s) for s in SUBREDDITS])
    db.session.commit()


def reddit_client():
    return praw.Reddit(client_id=REDDIT_CLIENT_ID,
                       client_secret=REDDIT_CLIENT_SECRET,
                       username=REDDIT_USERNAME,
                       password=REDDIT_PASSWORD,
                       user_agent='Orangered 1.0 (by /u/deneb150)')


def send_emails():
    _send_emails(_scrape_posts())
    if datetime.now().weekday() == 6:
        _send_emails(_scrape_posts('weekly'), 'weekly')


def _send_emails(subreddit_posts, interval='daily'):
    with app.app_context():
        for account in Account.query.join(Account.email_events).filter(
                *_account_filters(6 if interval == 'weekly' else None)):
            account_subreddit_posts = OrderedDict([
                (s.name, subreddit_posts[s.name])
                for s in account.email_events[0].subreddits])
            _send_email_for_account(account, account_subreddit_posts)


def _account_filters(day_of_week):
    return (
        Account.active.is_(True),
        (Account.last_email < datetime.utcnow() - timedelta(hours=23)) |
        Account.last_email.is_(None),
        (EmailEvent.day_of_week.is_(None) if day_of_week is None else
         EmailEvent.day_of_week == day_of_week),
    )


def _send_email_for_account(account, subreddit_posts):
    logging.info('Sending email to %s with subreddits: %s',
                 account.email, ', '.join(subreddit_posts.keys()))
    context = {
        'subreddits': subreddit_posts.items(),
        'email_management_url': url_for('manage', uuid=account.uuid),
        'unsubscribe_url': url_for('unsubscribe', uuid=account.uuid),
    }
    html_data = Template(HTML_TEMPLATE, trim_blocks=True).render(**context)
    text_data = Template(TEXT_TEMPLATE, trim_blocks=True).render(**context)
    _send_email(account.email, html_data, text_data)
    account.last_email = datetime.utcnow()
    db.session.commit()


def _send_email(email, html, text):
    if app.config['DEBUG']:
        return _save_test_emails(html, text)
    resp = requests.post(
        MAILGUN_API_URL,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": "Orangered <no-reply@orangered.io>",
            "to": [email],
            "subject": ("Orangered - "
                        "The best content from your favorite subreddits"),
            "html": html,
            "text": text,
        })
    resp.raise_for_status()


def _save_test_emails(html, text):
    with open('test_email.html', 'w') as h, open('test_email.txt', 'w') as t:
        logging.debug('saving test_email.html')
        h.write(html)
        logging.debug('saving test_email.txt')
        t.write(text)
        return


def _scrape_posts(interval='daily'):
    logging.info(f'Scraping subreddit posts for {interval} interval')
    reddit = reddit_client()
    subreddit_posts = {}
    now = datetime.utcnow()
    for subreddit in _subreddits_to_scrape(
            6 if interval == 'weekly' else None):
        if interval == 'daily':
            posts = _daily_top_posts(reddit, subreddit, now)
        else:
            posts = _weekly_top_posts(reddit, subreddit, now)
        subreddit_posts[subreddit.name] = posts
    logging.info('Done scraping subreddit posts')
    return subreddit_posts


def _daily_top_posts(reddit, subreddit, now):
    if subreddit.last_scraped_daily and (
            subreddit.last_scraped_daily > now - timedelta(hours=23)):
        logging.info('Subreddit: %s recently scraped for daily top '
                     'posts, loading existing posts', subreddit.name)
        return _existing_scraped_posts(subreddit, now, 'daily')
    else:
        logging.info('Scraping new daily top posts for subreddit: %s',
                     subreddit.name)
        return _scrape_new_posts(reddit, subreddit, 'daily')


def _weekly_top_posts(reddit, subreddit, now):
    if subreddit.last_scraped_weekly and (
            subreddit.last_scraped_weekly > now - timedelta(hours=23)):
        logging.info('Subreddit: %s recently scraped for weekly top '
                     'posts, loading existing posts', subreddit.name)
        return _existing_scraped_posts(subreddit, now, 'weekly')
    else:
        logging.info('Scraping new weekly top posts for subreddit: %s',
                     subreddit.name)
        return _scrape_new_posts(reddit, subreddit, 'weekly')


def _existing_scraped_posts(subreddit, now, interval):
    query = SubredditPost.query.filter(
        SubredditPost.subreddit == subreddit,
        SubredditPost.scraped_at > now - timedelta(hours=23),
    )
    if interval == 'daily':
        query.filter(SubredditPost.daily_top.is_(True))
    elif interval == 'weekly':
        query.filter(SubredditPost.weekly_top.is_(True))
    return query.all()


def _scrape_new_posts(reddit, subreddit, interval):
    posts = []
    for post in reddit.subreddit(subreddit.name).top(
            'day' if interval == 'daily' else 'week', limit=10):
        if interval == 'daily' and not SubredditPost.query.filter(
            SubredditPost.id == post.id,
            SubredditPost.daily_top.is_(True),
        ).one_or_none():
            existing_post = SubredditPost.query.get(post.id)
            if existing_post:
                existing_post.daily_top = True
                posts.append(existing_post)
            else:
                logging.info(f'Scraping daily top post: {post.id}')
                posts.append(SubredditPost(
                    id=post.id,
                    url=post.url,
                    title=post.title,
                    subreddit=subreddit,
                    preview_image_url=_get_post_preview(post),
                    permalink_url=_get_permalink_url(post),
                    num_comments=post.num_comments,
                    daily_top=True,
                ))
        elif interval == 'weekly' and not SubredditPost.query.filter(
            SubredditPost.id == post.id,
            SubredditPost.weekly_top.is_(True),
        ).one_or_none():
            existing_post = SubredditPost.query.get(post.id)
            if existing_post:
                existing_post.weekly_top = True
                posts.append(existing_post)
            else:
                logging.info(f'Scraping weekly top post: {post.id}')
                posts.append(SubredditPost(
                    id=post.id,
                    url=post.url,
                    title=post.title,
                    subreddit=subreddit,
                    preview_image_url=_get_post_preview(post),
                    permalink_url=_get_permalink_url(post),
                    num_comments=post.num_comments,
                    weekly_top=True,
                ))
    db.session.add_all(posts)
    if interval == 'daily':
        subreddit.last_scraped_daily = datetime.utcnow()
    elif interval == 'weekly':
        subreddit.last_scraped_weekly = datetime.utcnow()
    db.session.commit()
    return posts


def _get_post_preview(post):
    if not hasattr(post, 'preview') or not post.preview:
        return
    for image in reversed(post.preview['images'][0]['resolutions']):
        if image['width'] < 800:
            return image['url']


def _get_permalink_url(post):
    if post.is_self:
        return
    return f'https://www.reddit.com{post.permalink}'


def _subreddits_to_scrape(day_of_week):
    return Subreddit.query.join(Subreddit.email_events).join(Account).filter(
        *_account_filters(day_of_week))
