import unittest
import jwt

from src.classes.login import Login
from src.classes.user import User
from src.classes.customer import Customer
from src.classes.mongo_engine import MongoEngine
from tests.utils.auth import Auth
from config.server_environment import TESTING_DATABASE, JWT_ENC_KEY


class UserTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(UserTests, self).__init__(*args, **kwargs)

        # Drop previous database
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'users')

    def test_login_existing_user(self):
        User().insert({
            'type': 'admin',
            'first_name': 'Admin',
            'last_name': '1',
            'username': 'admin1',
            'email': 'admin1@domain.com',
            'password': 'admin1'
        })

        logged_user = Login().login(Auth('admin1', 'admin1'))

        self.assertNotEqual(logged_user, None, 'Existing user not logged in')

    def test_login_non_existing_user(self):
        logged_user = Login().login(Auth('123', '456'))

        self.assertEqual(logged_user, False, 'Non existing user logged in')

    def test_logout_non_logged_in_user(self):
        status = Login().logout('admin1')

        self.assertEqual(status, False, 'Non existing user not logged out')

    def test_login_and_logout(self):
        User().insert({
            'type': 'admin',
            'first_name': 'Admin',
            'last_name': '1',
            'username': 'admin1',
            'email': 'admin1@domain.com',
            'password': 'admin1'
        })

        logged_user = Login().login(Auth('admin1', 'admin1'))
        self.assertNotEqual(logged_user, None, 'Existing user not logged in')

        status = Login().logout('admin1')
        self.assertEqual(status, True, 'Non existing user not logged out')

    def test_check_logged_user_props(self):
        u = {
            'type': 'admin',
            'first_name': 'Admin',
            'last_name': '1',
            'username': 'admin1',
            'email': 'admin1@domain.com',
            'password': 'admin1'
        }

        keys = ['_id', 'public_id', 'token', 'username', 'exp', 'login_time']

        User().insert(u)
        user = User().find({'username': 'admin1'})
        logged_user = Login().login(Auth('admin1', 'admin1'))
        self.assertNotEqual(logged_user, None, 'Logged user obj not created')
        self.assertIsInstance(logged_user.data, dict,
                              'User data is not a dict')
        self.assertListEqual(list(logged_user.data.keys()), keys,
                             'Keys are not equal')

        self.assertEqual(logged_user.data['public_id'], user.data['public_id'],
                         'Public id not equal')
        self.assertEqual(logged_user.data['username'], user.data['username'],
                         'Username not equal')

    def test_token(self):
        u = {
            'type': 'admin',
            'first_name': 'Admin',
            'last_name': '1',
            'username': 'admin1',
            'email': 'admin1@domain.com',
            'password': 'admin1'
        }

        keys = ['_id', 'public_id', 'token', 'username', 'exp',
                'login_time']

        User().insert(u)
        logged_user = Login().login(Auth('admin1', 'admin1'))
        self.assertNotEqual(logged_user, None, 'Logged user obj not created')
        self.assertIsInstance(logged_user.data, dict,
                              'User data is not a dict')
        self.assertListEqual(list(logged_user.data.keys()), keys,
                             'Keys are not equal')

        token = logged_user.data['token']
        data = jwt.decode(token, JWT_ENC_KEY, algorithms=['HS256'])

        self.assertEqual(logged_user.data['public_id'],
                         data['public_id'], 'Public id from token not equal')
