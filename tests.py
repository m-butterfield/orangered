from datetime import datetime, timedelta
from itertools import chain
import unittest
from unittest import mock
import uuid

from app import app, db, Account, Subreddit, SubredditPost
from subreddits import insert_subreddits
from utils import _scrape_posts, _send_emails


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        db.close_all_sessions()
        db.drop_all()
        db.create_all()
        insert_subreddits()


class AppTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.client = app.test_client()
        self.account = Account(email='bob@aol.com')
        db.session.add(self.account)
        db.session.commit()

    def test_valid_signup(self):
        expected_subreddits = ['aviation', 'spacex']
        resp = self.client.post('/signup', data={
            'email': 'bob2@aol.com',
            'subreddits[]': expected_subreddits,
        })
        self.assertEqual(resp.status_code, 201)
        account = Account.query.get('bob2@aol.com')
        self.assertIsNotNone(account)
        self.assertTrue(account.active)
        self.assertEqual(
            set(expected_subreddits), {s.name for s in account.subreddits})

    def test_unsubscribe_not_found(self):
        resp = self.client.post('/email/blah/unsubscribe')
        self.assertEqual(resp.status_code, 404)

    def test_unsubscribe(self):
        resp = self.client.post(f'/account/{self.account.uuid}/unsubscribe',
                                data={'unsubscribe': 'True'})
        self.assertEqual(resp.status_code, 200)
        db.session.add(self.account)
        self.assertFalse(self.account.active)

        # resubscribe
        resp = self.client.post(f'/account/{self.account.uuid}/unsubscribe',
                                data={'unsubscribe': 'False'})
        self.assertEqual(resp.status_code, 200)
        db.session.add(self.account)
        self.assertTrue(self.account.active)


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
    @mock.patch('utils.Template')
    @mock.patch('utils._send_email')
    def test_scrape_and_send_emails(self, fake_send_email, fake_template, _):
        # user account with some subscriptions
        db.session.add(Account(
            email='bob@aol.com',
            subreddits=Subreddit.query.filter(Subreddit.name.in_(
                ['aviation', 'spacex', 'running'])).all(),
        ))
        # another that is deactivated
        db.session.add(Account(
            email='bob2@aol.com',
            subreddits=Subreddit.query.filter(Subreddit.name.in_(
                ['programming', 'AskReddit'])).all(),
            active=False,
        ))

        # spacex will have last_scraped = None so scraping should happen
        self.assertIsNone(Subreddit.query.get('spacex').last_scraped)
        # set last scraped past one day for running so scraping should happen
        Subreddit.query.get('running').last_scraped = (
                datetime.utcnow() - timedelta(days=2))
        # aviation has already been scraped so add some existing scraped posts
        now = datetime.utcnow()
        Subreddit.query.get('aviation').last_scraped = now
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

        subreddit_posts = _scrape_posts()
        self.assertSetEqual(
            {'aviation', 'spacex', 'running'}, set(subreddit_posts.keys()))
        self.assertEqual(len(subreddit_posts['aviation']), 2)
        self.assertEqual(len(subreddit_posts['spacex']), 5)
        self.assertEqual(len(subreddit_posts['running']), 5)
        self.assertIsNotNone(Subreddit.query.get('spacex').last_scraped)
        self.assertGreaterEqual(
            Subreddit.query.get('running').last_scraped, now)
        self.assertEqual(Subreddit.query.get('aviation').last_scraped, now)

        _send_emails(subreddit_posts)
        db.session.add_all(chain.from_iterable(subreddit_posts.values()))
        fake_template().render.assert_called_with(
            email_management_url='',
            unsubscribe_url=mock.ANY,
            subreddits=[
                ('aviation', subreddit_posts['aviation']),
                ('running', subreddit_posts['running']),
                ('spacex', subreddit_posts['spacex']),
            ],
        )
        fake_send_email.assert_called_once_with(
            'bob@aol.com', mock.ANY, mock.ANY)
