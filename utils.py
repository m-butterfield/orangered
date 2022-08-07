from collections import OrderedDict
from datetime import datetime, timedelta
import logging
import os

from flask import url_for
from jinja2 import Template
import praw
from bs4 import BeautifulSoup
import requests
from sendgrid import From, Mail, SendGridAPIClient

from app import (
    Account,
    app,
    db,
    EmailEvent,
    ScrapeRecord,
    ScrapeRecordSubredditPost,
    Subreddit,
    SubredditPost,
)

from subreddits import SUBREDDITS


REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.environ.get("REDDIT_USERNAME")
REDDIT_PASSWORD = os.environ.get("REDDIT_PASSWORD")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


def _html_template():
    with open("templates/email.html") as fp:
        return fp.read()


def _text_template():
    with open("templates/email.txt") as fp:
        return fp.read()


HTML_TEMPLATE, TEXT_TEMPLATE = _html_template(), _text_template()


def insert_subreddits():
    for s in [Subreddit(name=s) for s in SUBREDDITS]:
        db.session.merge(s)
    db.session.commit()


def reddit_client():
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        user_agent="Orangered 1.0 (by /u/deneb150)",
    )


def send_emails():
    _send_emails(_scrape_posts())
    if datetime.now().weekday() == 6:
        _send_emails(_scrape_posts("weekly"), "weekly")


def _send_emails(subreddit_posts, interval="daily"):
    with app.app_context():
        for account in Account.query.join(Account.email_events).filter(
            *_account_filters(6 if interval == "weekly" else None)
        ):
            account_subreddit_posts = OrderedDict(
                [
                    (s.name, subreddit_posts[s.name])
                    for s in account.email_events[0].subreddits
                ]
            )
            _send_email_for_account(account, account_subreddit_posts)


def _account_filters(day_of_week):
    return (
        Account.active.is_(True),
        (Account.last_email < datetime.utcnow() - timedelta(hours=23))
        | Account.last_email.is_(None),
        (
            EmailEvent.day_of_week.is_(None)
            if day_of_week is None
            else EmailEvent.day_of_week == day_of_week
        ),
    )


def _send_email_for_account(account, subreddit_posts):
    logging.info(
        "Sending email to %s with subreddits: %s",
        account.email,
        ", ".join(subreddit_posts.keys()),
    )
    context = {
        "subreddits": subreddit_posts.items(),
        "email_management_url": url_for("manage", uuid=account.uuid),
        "unsubscribe_url": url_for("unsubscribe", uuid=account.uuid),
    }
    html_data = Template(HTML_TEMPLATE, trim_blocks=True).render(**context)
    text_data = Template(TEXT_TEMPLATE, trim_blocks=True).render(**context)
    _send_email(account.email, html_data, text_data)
    account.last_email = datetime.utcnow()
    db.session.commit()


def _send_email(email, html, text):
    if app.config["DEBUG"]:
        return _save_test_emails(html, text)
    SendGridAPIClient(os.environ.get("SENDGRID_API_KEY")).send(
        Mail(
            from_email=From("postman@orangered.email", "Orangered"),
            to_emails=email,
            subject="Orangered - " "The best content from your favorite subreddits",
            html_content=html,
            plain_text_content=text,
        )
    )


def _save_test_emails(html, text):
    with open("test_email.html", "w") as h, open("test_email.txt", "w") as t:
        logging.debug("saving test_email.html")
        h.write(html)
        logging.debug("saving test_email.txt")
        t.write(text)
        return


def _scrape_posts(interval="daily"):
    logging.info(f"Scraping subreddit posts for {interval} interval")
    reddit = reddit_client()
    subreddit_posts = {}
    now = datetime.utcnow()
    for subreddit in _subreddits_to_scrape(6 if interval == "weekly" else None):
        scrape_record = ScrapeRecord.query.filter(
            ScrapeRecord.subreddit == subreddit,
            ScrapeRecord.interval == interval,
            ScrapeRecord.scrape_time > now - timedelta(hours=23),
        ).one_or_none()
        if not scrape_record:
            logging.info(
                f"Scraping new {interval} top posts for " f"subreddit: {subreddit.name}"
            )
            scrape_record = _scrape_new_posts(reddit, subreddit, interval)
        subreddit_posts[subreddit.name] = scrape_record.subreddit_posts
    logging.info("Done scraping subreddit posts")
    return subreddit_posts


def _scrape_new_posts(reddit, subreddit, interval):
    posts = []
    for post in reddit.subreddit(subreddit.name).top(
        "day" if interval == "daily" else "week", limit=10
    ):
        existing_post = SubredditPost.query.get(post.id)
        if existing_post:
            if any(sr.interval == interval for sr in existing_post.scrape_records):
                continue
            existing_post.daily_top = True
            existing_post.scraped_at = datetime.utcnow()
            existing_post.num_comments = post.num_comments
            posts.append(existing_post)
        else:
            logging.info(f"Scraping daily top post: {post.id}")
            posts.append(
                SubredditPost(
                    id=post.id,
                    url=post.url,
                    title=post.title,
                    subreddit=subreddit,
                    preview_image_url=_get_post_preview(post),
                    permalink_url=_get_permalink_url(post),
                    num_comments=post.num_comments,
                )
            )
    scrape_record = ScrapeRecord(
        interval=interval,
        subreddit=subreddit,
        scrape_record_subreddit_posts=[
            ScrapeRecordSubredditPost(ordinal=i, subreddit_post=subreddit_post)
            for i, subreddit_post in enumerate(posts)
        ],
    )
    db.session.add(scrape_record)
    db.session.commit()
    return scrape_record


def _get_post_preview(post):
    if not hasattr(post, "preview") or not post.preview:
        return
    for image in reversed(post.preview["images"][0]["resolutions"]):
        if image["width"] < 800:
            return image["url"]


def _get_permalink_url(post):
    if post.is_self:
        return
    return f"https://www.reddit.com{post.permalink}"


def _subreddits_to_scrape(day_of_week):
    return (
        Subreddit.query.join(Subreddit.email_events)
        .join(Account)
        .filter(*_account_filters(day_of_week))
    )


def scrape_subreddits():
    with app.app_context():
        _scrape_subreddits()


def _scrape_subreddits():
    resp = requests.get(
        "https://www.reddit.com/subreddits",
        headers={"User-agent": "orangered 0.1"},
    )
    resp.raise_for_status()
    count = 25
    results = BeautifulSoup(resp.content, "html.parser").find_all(
        "p", class_="titlerow"
    )
    while results:
        subreddits = []
        for title_row in results:
            link = title_row.find("a")
            subreddits.append(link.getText()[2:].split(":")[0])

        for s in [Subreddit(name=s) for s in subreddits]:
            db.session.merge(s)
        db.session.commit()

        subreddit_id = (
            title_row.find_next_sibling().find("form").find("input").attrs["value"]
        )
        resp = requests.get(
            f"https://www.reddit.com/subreddits/?app=res&count={count}&after={subreddit_id}",
            headers={"User-agent": "orangered 0.1"},
        )
        resp.raise_for_status()
        results = BeautifulSoup(resp.content, "html.parser").find_all(
            "p", class_="titlerow"
        )
        count += 25
