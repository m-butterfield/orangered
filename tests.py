from datetime import datetime, timedelta
import unittest
from unittest import mock
import uuid

from application import application, db, Account, Subreddit, SubredditPost
from subreddits import insert_subreddits
from utils import scrape_posts


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.close_all_sessions()
        db.drop_all()
        db.create_all()
        insert_subreddits()


class AppTests(BaseTestCase):

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

    def __init__(self, name):
        self.name = name

    def top(self, *args, **kwargs):
        return [FakeSubredditPost(f'{self.name} post {i}') for i in range(5)]


class FakeReddit:

    def __init__(self):
        self._subreddits = {
            'spacex': FakeSubreddit('spacex'),
            'running': FakeSubreddit('running'),
        }

    def subreddit(self, name):
        return self._subreddits[name]


class EmailTests(BaseTestCase):

    @mock.patch('utils._reddit', return_value=FakeReddit())
    def test_scrape_posts(self, _):
        # user account with some subscriptions
        db.session.add(Account(
            email='bob@aol.com',
            subreddits=db.session.query(Subreddit).filter(Subreddit.name.in_(
                    ['aviation', 'spacex', 'running'])).all(),
        ))

        # spacex will have last_scraped = None so scraping should happen
        self.assertIsNone(
            db.session.query(Subreddit).get('spacex').last_scraped)
        # set last scraped past one day for running so scraping should happen
        db.session.query(Subreddit).get('running').last_scraped = (
                datetime.utcnow() - timedelta(days=2))
        # aviation has already been scraped so add some existing scraped posts
        now = datetime.utcnow()
        db.session.query(Subreddit).get('aviation').last_scraped = now
        # add existing posts for aviation
        db.session.add_all([
            SubredditPost(
                id=str(uuid.uuid4()),
                subreddit_name='aviation',
                title='aviation post 1',
                url='http://example.com',
                scraped_at=datetime.utcnow(),
            ),
            SubredditPost(
                id=str(uuid.uuid4()),
                subreddit_name='aviation',
                title='aviation post 2',
                url='http://example.com',
                scraped_at=datetime.utcnow(),
            ),
            SubredditPost(
                id=str(uuid.uuid4()),
                subreddit_name='aviation',
                title='aviation post 3',
                url='http://example.com',
                # this post from a previous day shouldn't show up in the result
                scraped_at=datetime.utcnow() - timedelta(days=1),
            ),
        ])
        db.session.commit()

        subreddits = scrape_posts()
        self.assertSetEqual(
            {'aviation', 'spacex', 'running'}, set(subreddits.keys()))
        self.assertEqual(len(subreddits['aviation']), 2)
        self.assertEqual(len(subreddits['spacex']), 5)
        self.assertEqual(len(subreddits['running']), 5)
        self.assertIsNotNone(
            db.session.query(Subreddit).get('spacex').last_scraped)
        self.assertGreaterEqual(
            db.session.query(Subreddit).get('running').last_scraped, now)
        self.assertEqual(
            db.session.query(Subreddit).get('aviation').last_scraped, now)
