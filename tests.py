import unittest
from unittest import mock

from application import application, db, Account, Subreddit
from utils import send_emails


class AppTests(unittest.TestCase):

    def setUp(self):
        self.client = application.test_client()

    def test_valid_signup(self):
        expected_subreddits = ['aviation', 'spacex']
        resp = self.client.post('/signup', data={
            'email': 'bob@aol.com',
            'subreddits': expected_subreddits,
        })
        self.assertEqual(resp.status_code, 201)
        account = db.session.query(Account).get('bob@aol.com')
        self.assertIsNotNone(account)
        self.assertEqual(
            set(expected_subreddits), {s.name for s in account.subreddits})


class EmailTests(unittest.TestCase):

    @mock.patch('utils.Template')
    def test_send_emails(self, fake_template):
        db.session.add(Account(
            email='bob@aol.com',
            subreddits=db.session.query(Subreddit).filter(Subreddit.name.in_(
                    ['aviation', 'spacex'])).all(),
        ))
        db.session.commit()
        send_emails()
