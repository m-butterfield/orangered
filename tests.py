import unittest

from app import app, db, User


class AppTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_valid_signup(self):
        expected_subreddits = ['aviation', 'spacex']
        resp = self.client.post('/signup', data={
            'email': 'bob@aol.com',
            'subreddits': expected_subreddits,
        })
        self.assertEqual(resp.status_code, 201)
        user = db.session.query(User).get('bob@aol.com')
        self.assertIsNotNone(user)
        self.assertEqual(
            set(expected_subreddits), {s.name for s in user.subreddits})
