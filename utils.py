from collections import OrderedDict
from datetime import datetime, timedelta
import logging
import os

from flask import url_for

from jinja2 import Template

import praw

import requests

from app import (
    Account,
    app,
    db,
    EmailEvent,
    EmailEventSubreddit,
    ScrapeRecord,
    ScrapeRecordSubredditPost,
    Subreddit,
    SubredditPost,
)

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
                ((e.subreddit_name, e.search_term),
                 subreddit_posts[(e.subreddit_name, e.search_term)])
                for e in account.email_events[0].email_event_subreddits])
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
    logging.info('Sending email to %s with subreddit search terms: %s',
                 account.email, subreddit_posts.keys())
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
    for subreddit_name, search_term in _subreddit_terms_to_scrape(
            6 if interval == 'weekly' else None):
        scrape_record = ScrapeRecord.query.filter(
            ScrapeRecord.subreddit_name == subreddit_name,
            ScrapeRecord.search_term == search_term,
            ScrapeRecord.interval == interval,
            ScrapeRecord.scrape_time > now - timedelta(hours=23),
        ).one_or_none()
        if not scrape_record:
            logging.info(f'Scraping new {interval} top posts for '
                         f'subreddit: {subreddit_name} '
                         f'search_term: {search_term}')
            scrape_record = _scrape_new_posts(
                reddit, subreddit_name, search_term, interval)
        subreddit_posts[(
            subreddit_name, search_term)] = scrape_record.subreddit_posts
    logging.info('Done scraping subreddit posts')
    return subreddit_posts


def _scrape_new_posts(reddit, subreddit_name, search_term, interval):
    posts = []
    time_filter = 'day' if interval == 'daily' else 'week'
    if search_term:
        results = reddit.subreddit(subreddit_name).search(
            search_term, time_filter=time_filter, limit=10)
    else:
        results = reddit.subreddit(subreddit_name).top(time_filter, limit=10)
    for post in results:
        existing_post = SubredditPost.query.get(post.id)
        if existing_post:
            if any(sr.interval == interval
                   for sr in existing_post.scrape_records):
                continue
            existing_post.daily_top = True
            existing_post.scraped_at = datetime.utcnow()
            existing_post.num_comments = post.num_comments
            posts.append(existing_post)
        else:
            logging.info(f'Scraping post: {post.id}')
            posts.append(SubredditPost(
                id=post.id,
                url=post.url,
                title=post.title,
                subreddit_name=subreddit_name,
                preview_image_url=_get_post_preview(post),
                permalink_url=_get_permalink_url(post),
                num_comments=post.num_comments,
            ))
    scrape_record = ScrapeRecord(
        interval=interval,
        subreddit_name=subreddit_name,
        search_term=search_term,
        scrape_record_subreddit_posts=[
            ScrapeRecordSubredditPost(
                ordinal=i,
                subreddit_post=subreddit_post
            )
            for i, subreddit_post in enumerate(posts)
        ]
    )
    db.session.add(scrape_record)
    db.session.commit()
    return scrape_record


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


def _subreddit_terms_to_scrape(day_of_week):
    ees_cols = (
        EmailEventSubreddit.subreddit_name, EmailEventSubreddit.search_term)
    return db.session.query(*ees_cols).distinct(*ees_cols).order_by(
        *ees_cols).join(EmailEventSubreddit.account).filter(
        *_account_filters(day_of_week))
