from datetime import datetime, timedelta
import unittest
from unittest import mock
import uuid

from application import application, db, Account, Subreddit
from utils import scrape_posts


class AppTests(unittest.TestCase):

    def setUp(self):
        self.client = application.test_client()

    def test_valid_signup(self):
        expected_subreddits = ['aviation', 'spacex']
        resp = self.client.post('/signup', data={
            'email': 'bob@aol.com',
            'subreddits[]': expected_subreddits,
        })
        self.assertEqual(resp.status_code, 201)
        account = db.session.query(Account).get('bob@aol.com')
        self.assertIsNotNone(account)
        self.assertEqual(
            set(expected_subreddits), {s.name for s in account.subreddits})


class FakeSubredditPost:

    def __init__(self, title):
        self.id = str(uuid.uuid4())
        self.url = 'http://example.com'
        self.title = title


class FakeSubreddit:

    def __init__(self, name, last_scraped=None):
        self.name = name
        self.last_scraped = last_scraped

    def top(self, *args, **kwargs):
        return [FakeSubredditPost(f'{self.name} post {i}') for i in range(5)]


class FakeReddit:

    def __init__(self):
        self._subreddits = {
            'aviation': FakeSubreddit(
                'aviation',
                last_scraped=datetime.utcnow() - timedelta(days=1),
            ),
            'spacex': FakeSubreddit('spacex'),
        }

    def subreddit(self, name):
        return self._subreddits[name]


class EmailTests(unittest.TestCase):

    @mock.patch('utils._reddit', return_value=FakeReddit())
    def test_scrape_posts(self, _):
        db.session.add(Account(
            email='bob@aol.com',
            subreddits=db.session.query(Subreddit).filter(Subreddit.name.in_(
                    ['aviation', 'spacex'])).all(),
        ))
        db.session.commit()
        subreddits = scrape_posts()
        self.assertSetEqual({'aviation', 'spacex'}, set(subreddits.keys()))
