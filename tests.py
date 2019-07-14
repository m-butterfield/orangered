from collections import OrderedDict
from datetime import datetime, time, timedelta
from itertools import chain
import unittest
from unittest import mock
import uuid

from freezegun import freeze_time

from app import app, db, Account, EmailEvent, Subreddit, SubredditPost
from utils import insert_subreddits
from utils import _scrape_posts, _send_emails


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        db.close_all_sessions()
        db.drop_all()
        db.create_all()
        insert_subreddits()


class BaseAppTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.client = app.test_client()
        self.account = Account(
            email='bob@aol.com',
            email_events=[EmailEvent(
                account_email='bob@aol.com',
                time_of_day=time(12),
            )],
        )
        db.session.add(self.account)
        db.session.commit()


class SignupTests(BaseAppTestCase):

    def test_valid_signup(self):
        expected_subreddits = ['aviation', 'spacex']
        resp = self.client.post('/signup', data={
            'email': 'Bob2@aol.com',
            'subreddits[]': expected_subreddits,
            'email_interval': 'weekly',
        })
        self.assertEqual(resp.status_code, 201)
        account = Account.query.get('bob2@aol.com')
        self.assertIsNotNone(account)
        self.assertTrue(account.active)
        self.assertEqual(len(account.email_events), 1)
        self.assertEqual(account.email_events[0].time_of_day, time(12))
        self.assertEqual(account.email_events[0].day_of_week, 6)
        self.assertEqual(
            set(expected_subreddits),
            {s.name for s in account.email_events[0].subreddits})

        self.client.post('/signup', data={
            'email': 'Bob3@aol.com',
            'subreddits[]': expected_subreddits,
            'email_interval': 'daily',
        })
        account = Account.query.get('bob3@aol.com')
        self.assertIsNone(account.email_events[0].day_of_week)

    def test_account_already_exists(self):
        resp = self.client.post('/signup', data={
            'email': self.account.email,
            'subreddits[]': ['aviation'],
        })
        self.assertEqual(resp.status_code, 400)

    def test_max_10_subreddits(self):
        resp = self.client.post('/signup', data={
            'email': 'bob2@aol.com',
            'subreddits[]': ['aviation'] * 11,
        })
        self.assertEqual(resp.status_code, 400)


class UnsubscribeTests(BaseAppTestCase):

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


class ManageTests(BaseAppTestCase):

    def test_redirect_to_unsubscribe(self):
        self.account.active = False
        db.session.commit()
        resp = self.client.get(f'/account/{self.account.uuid}/manage')
        self.assertEqual(resp.status_code, 302)

    def test_max_10_subreddits(self):
        resp = self.client.post(f'/account/{self.account.uuid}/manage', data={
            'subreddits[]': ['aviation'] * 11})
        self.assertEqual(resp.status_code, 400)

    def test_update_account(self):
        expected_subreddits = ['aviation', 'spacex', 'analog']
        resp = self.client.post(f'/account/{self.account.uuid}/manage', data={
            'subreddits[]': expected_subreddits,
            'email_interval': 'weekly',
        })
        self.assertEqual(resp.status_code, 200)
        account = Account.query.get(self.account.email)
        self.assertEqual(len(account.email_events), 1)
        self.assertEqual(account.email_events[0].time_of_day, time(12))
        self.assertEqual(account.email_events[0].day_of_week, 6)
        self.assertEqual(
            set(expected_subreddits),
            {s.name for s in account.email_events[0].subreddits})

        self.client.post(f'/account/{self.account.uuid}/manage', data={
            'subreddits[]': expected_subreddits,
            'email_interval': 'daily',
        })
        account = Account.query.get(self.account.email)
        self.assertEqual(len(account.email_events), 1)
        self.assertEqual(account.email_events[0].time_of_day, time(12))
        self.assertIsNone(account.email_events[0].day_of_week)


class FakeSubredditPost:

    def __init__(self, subreddit_name, post_number):
        self.id = f'{subreddit_name}_{post_number}'
        self.url = 'http://example.com'
        self.title = f'{subreddit_name} post {post_number}'
        self.num_comments = 23
        self.permalink = f'/r/{subreddit_name}/comments/abc123/cool_post/'
        self.is_self = False

    @property
    def preview(self):
        return {
            'enabled': True,
            'images': [{
                'id': '1234567890abcdefGHIJKLMNOPQRSTUVWXYz0123456',
                'resolutions': [
                    {
                        'height': 66,
                        'url': 'https://preview.redd.it/1.jpg',
                        'width': 108,
                    }, {
                        'height': 133,
                        'url': 'https://preview.redd.it/2.jpg',
                        'width': 216,
                    }, {
                        'height': 197,
                        'url': 'https://preview.redd.it/3.jpg',
                        'width': 320,
                    }, {
                        'height': 395,
                        'url': 'https://preview.redd.it/4.jpg',
                        'width': 640,
                    }, {
                        'height': 592,
                        'url': 'https://preview.redd.it/5.jpg',
                        'width': 960,
                    }, {
                        'height': 666,
                        'url': 'https://preview.redd.it/6.jpg',
                        'width': 1080,
                    },
                ],
                'source': {
                    'height': 3514,
                    'url': 'https://preview.redd.it/zbdl7wi19h031.jpg?auto=webp&s=3d18c3607a9463c787b8f32fc122c529bc73a716',
                    'width': 5691,
                },
                'variants': {},
            }],
        }


class FakeSubreddit:

    def __init__(self, name, interval):
        self.name = name
        self.interval = interval

    def top(self, interval, *args, **kwargs):
        if interval == self.interval:
            return [FakeSubredditPost(self.name, i) for i in range(5)]


class FakeReddit:

    def __init__(self, interval):
        self._subreddits = {
            'spacex': FakeSubreddit('spacex', interval),
            'running': FakeSubreddit('running', interval),
        }

    def subreddit(self, name):
        return self._subreddits[name]


class EmailTests(BaseTestCase):

    @mock.patch('utils.Template')
    @mock.patch('utils._send_email')
    @freeze_time("2019-06-08 12:00:00")
    def test_scrape_and_send_daily_emails(self, fake_send_email, fake_template):
        # user account with some subscriptions
        db.session.add(Account(
            email='bob@aol.com',
            email_events=[EmailEvent(
                account_email='bob@aol.com',
                time_of_day=time(12),
                subreddits=Subreddit.query.filter(Subreddit.name.in_(
                    ['aviation', 'spacex', 'running'])).all(),
            )],
        ))
        # deactivated account
        db.session.add(Account(
            email='bob2@aol.com',
            active=False,
            email_events=[EmailEvent(
                account_email='bob@aol.com',
                time_of_day=time(12),
                subreddits=Subreddit.query.filter(Subreddit.name.in_(
                    ['programming', 'askreddit'])).all(),
            )],
        ))
        # account that already received their email for today
        db.session.add(Account(
            email='bob3@aol.com',
            last_email=datetime.utcnow() - timedelta(minutes=10),
            email_events=[EmailEvent(
                account_email='bob@aol.com',
                time_of_day=time(12),
                subreddits=Subreddit.query.filter(Subreddit.name.in_(
                    ['analog', 'finance'])).all(),
            )],
        ))
        # account expecting only weekly emails
        db.session.add(Account(
            email='bob4@aol.com',
            email_events=[EmailEvent(
                account_email='bob@aol.com',
                time_of_day=time(12),
                day_of_week=6,
                subreddits=Subreddit.query.filter(Subreddit.name.in_(
                    ['aviation', 'spacex', 'running'])).all(),
            )],
        ))

        # spacex will have last_scraped = None so scraping should happen
        self.assertIsNone(Subreddit.query.get('spacex').last_scraped_daily)
        # set last scraped past one day for running so scraping should happen
        Subreddit.query.get('running').last_scraped_daily = (
                datetime.utcnow() - timedelta(days=2))
        # aviation has already been scraped so add some existing scraped posts
        now = datetime.utcnow()
        Subreddit.query.get('aviation').last_scraped_daily = now
        # add existing posts for aviation
        db.session.add_all([
            SubredditPost(
                id=str(uuid.uuid4()),
                subreddit_name='aviation',
                title='aviation post 1',
                url='http://example.com',
                scraped_at=datetime.utcnow(),
                num_comments=23,
                daily_top=True,
            ),
            SubredditPost(
                id=str(uuid.uuid4()),
                subreddit_name='aviation',
                title='aviation post 2',
                url='http://example.com',
                scraped_at=datetime.utcnow(),
                num_comments=23,
                daily_top=True,
            ),
            SubredditPost(
                id=str(uuid.uuid4()),
                subreddit_name='aviation',
                title='aviation post 3',
                url='http://example.com',
                # this post from a previous day shouldn't show up in the result
                scraped_at=datetime.utcnow() - timedelta(days=1),
                num_comments=23,
                daily_top=True,
            ),
            # spacex post from previous day that shows up again
            SubredditPost(
                id='spacex_1',
                subreddit_name='spacex',
                title='aviation post 3',
                url='http://example.com',
                scraped_at=datetime.utcnow() - timedelta(days=1),
                num_comments=23,
                daily_top=True,
            ),
            # spacex post we already scraped from weekly scrape
            SubredditPost(
                id='spacex_2',
                subreddit_name='spacex',
                title='aviation post 3',
                url='http://example.com',
                scraped_at=datetime.utcnow() - timedelta(days=1),
                num_comments=23,
                weekly_top=True
            ),
        ])
        db.session.commit()

        with mock.patch('utils.reddit_client', return_value=FakeReddit(
            interval='day',
        )):
            subreddit_posts = _scrape_posts()
        self.assertSetEqual(
            {'aviation', 'spacex', 'running'}, set(subreddit_posts.keys()))
        self.assertEqual(len(subreddit_posts['aviation']), 2)
        self.assertEqual(len(subreddit_posts['spacex']), 4)
        self.assertEqual(len(subreddit_posts['running']), 5)
        self.assertTrue(SubredditPost.query.get('spacex_2').daily_top)
        self.assertTrue(SubredditPost.query.get('spacex_3').daily_top)
        self.assertIsNotNone(Subreddit.query.get('spacex').last_scraped_daily)
        self.assertGreaterEqual(
            Subreddit.query.get('running').last_scraped_daily, now)
        self.assertEqual(
            Subreddit.query.get('aviation').last_scraped_daily, now)

        _send_emails(subreddit_posts)
        db.session.add_all(chain.from_iterable(subreddit_posts.values()))
        fake_template().render.assert_called_with(
            email_management_url=mock.ANY,
            unsubscribe_url=mock.ANY,
            subreddits=OrderedDict([
                ('aviation', subreddit_posts['aviation']),
                ('running', subreddit_posts['running']),
                ('spacex', subreddit_posts['spacex']),
            ]).items(),
        )
        fake_send_email.assert_called_once_with(
            'bob@aol.com', mock.ANY, mock.ANY)
        self.assertAlmostEqual(Account.query.get('bob@aol.com').last_email,
                               now,
                               delta=timedelta(seconds=1))

    @mock.patch('utils.Template')
    @mock.patch('utils._send_email')
    @freeze_time("2019-06-09 12:00:00")
    def test_scrape_and_send_weekly_emails(self, fake_send_email, fake_template):
        # user account with some subscriptions
        db.session.add(Account(
            email='bob@aol.com',
            email_events=[EmailEvent(
                account_email='bob@aol.com',
                time_of_day=time(12),
                day_of_week=6,
                subreddits=Subreddit.query.filter(Subreddit.name.in_(
                    ['aviation', 'spacex', 'running'])).all(),
            )],
        ))
        # deactivated account
        db.session.add(Account(
            email='bob2@aol.com',
            active=False,
            email_events=[EmailEvent(
                account_email='bob@aol.com',
                time_of_day=time(12),
                day_of_week=6,
                subreddits=Subreddit.query.filter(Subreddit.name.in_(
                    ['programming', 'askreddit'])).all(),
            )],
        ))
        # account that already received their email for today
        db.session.add(Account(
            email='bob3@aol.com',
            last_email=datetime.utcnow() - timedelta(minutes=10),
            email_events=[EmailEvent(
                account_email='bob@aol.com',
                time_of_day=time(12),
                day_of_week=6,
                subreddits=Subreddit.query.filter(Subreddit.name.in_(
                    ['analog', 'finance'])).all(),
            )],
        ))
        # account expecting only daily emails
        db.session.add(Account(
            email='bob4@aol.com',
            email_events=[EmailEvent(
                account_email='bob@aol.com',
                time_of_day=time(12),
                subreddits=Subreddit.query.filter(Subreddit.name.in_(
                    ['aviation', 'spacex', 'running'])).all(),
            )],
        ))

        # spacex will have last_scraped = None so scraping should happen
        self.assertIsNone(Subreddit.query.get('spacex').last_scraped_weekly)
        # set last scraped past one day for running so scraping should happen
        Subreddit.query.get('running').last_scraped_weekly = (
                datetime.utcnow() - timedelta(days=2))
        # aviation has already been scraped so add some existing scraped posts
        now = datetime.utcnow()
        Subreddit.query.get('aviation').last_scraped_weekly = now
        # add existing posts for aviation
        db.session.add_all([
            SubredditPost(
                id=str(uuid.uuid4()),
                subreddit_name='aviation',
                title='aviation post 1',
                url='http://example.com',
                scraped_at=datetime.utcnow(),
                num_comments=23,
                weekly_top=True,
            ),
            SubredditPost(
                id=str(uuid.uuid4()),
                subreddit_name='aviation',
                title='aviation post 2',
                url='http://example.com',
                scraped_at=datetime.utcnow(),
                num_comments=23,
                weekly_top=True,
            ),
            SubredditPost(
                id=str(uuid.uuid4()),
                subreddit_name='aviation',
                title='aviation post 3',
                url='http://example.com',
                # this post from a previous day shouldn't show up in the result
                scraped_at=datetime.utcnow() - timedelta(days=1),
                num_comments=23,
                weekly_top=True,
            ),
            # spacex post from previous week that shows up again
            SubredditPost(
                id='spacex_1',
                subreddit_name='spacex',
                title='aviation post 3',
                url='http://example.com',
                scraped_at=datetime.utcnow() - timedelta(days=1),
                num_comments=23,
                weekly_top=True,
            ),
            # spacex post we already scraped from daily scrape
            SubredditPost(
                id='spacex_2',
                subreddit_name='spacex',
                title='aviation post 3',
                url='http://example.com',
                scraped_at=datetime.utcnow() - timedelta(days=1),
                num_comments=23,
                daily_top=True
            ),
        ])
        db.session.commit()

        with mock.patch('utils.reddit_client', return_value=FakeReddit(
            interval='week',
        )):
            subreddit_posts = _scrape_posts('weekly')
        self.assertSetEqual(
            {'aviation', 'spacex', 'running'}, set(subreddit_posts.keys()))
        self.assertEqual(len(subreddit_posts['aviation']), 2)
        self.assertEqual(len(subreddit_posts['spacex']), 4)
        self.assertEqual(len(subreddit_posts['running']), 5)
        self.assertTrue(SubredditPost.query.get('spacex_2').weekly_top)
        self.assertTrue(SubredditPost.query.get('spacex_3').weekly_top)
        self.assertIsNotNone(Subreddit.query.get('spacex').last_scraped_weekly)
        self.assertGreaterEqual(
            Subreddit.query.get('running').last_scraped_weekly, now)
        self.assertEqual(
            Subreddit.query.get('aviation').last_scraped_weekly, now)

        _send_emails(subreddit_posts, 'weekly')
        db.session.add_all(chain.from_iterable(subreddit_posts.values()))
        fake_template().render.assert_called_with(
            email_management_url=mock.ANY,
            unsubscribe_url=mock.ANY,
            subreddits=OrderedDict([
                ('aviation', subreddit_posts['aviation']),
                ('running', subreddit_posts['running']),
                ('spacex', subreddit_posts['spacex']),
            ]).items(),
        )
        fake_send_email.assert_called_once_with(
            'bob@aol.com', mock.ANY, mock.ANY)
        self.assertAlmostEqual(Account.query.get('bob@aol.com').last_email,
                               now,
                               delta=timedelta(seconds=1))
