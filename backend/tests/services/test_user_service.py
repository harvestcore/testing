import json
import unittest

from src.app import app
from src.classes.customer import Customer
from src.classes.user import User
from src.classes.mongo_engine import MongoEngine

from tests.utils.login import TestingLogin

from config.server_environment import TESTING_DATABASE


class UserServiceTests(unittest.TestCase):
    app = app.test_client()
    headers = TestingLogin().headers
    path = '/api/user'

    def setUp(self):
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'users')
        User().insert({
            'type': 'admin',
            'first_name': 'admin',
            'last_name': 'admin',
            'username': 'admin',
            'email': 'admin@domain.com',
            'password': 'admin'
        })

    def test_get_current_user(self):
        User().insert({
            'type': 'admin',
            'first_name': 'admin',
            'last_name': 'admin',
            'username': 'admin',
            'email': 'admin@domain.com',
            'password': 'admin'
        })

        response = self.app.get(
            self.path,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200, 'User not found')
        self.assertEqual(json.loads(response.data)['username'], 'admin',
                         'Wrong current user')

    def test_create_user(self):
        user = {
            'type': 'admin',
            'first_name': 'william',
            'last_name': 'william',
            'username': 'william',
            'email': 'william@domain.com',
            'password': 'william'
        }
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(user)
        )
        self.assertEqual(response.status_code, 200, 'User not created')

        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'email': 'william@domain.com'})
        )
        self.assertEqual(response.status_code, 204, 'User not deleted')

    def test_update_user(self):
        user = {
            'type': 'admin',
            'first_name': 'andrew',
            'last_name': 'andrew',
            'username': 'andrew',
            'email': 'andrew@domain.com',
            'password': 'andrew'
        }
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(user)
        )
        self.assertEqual(response.status_code, 200, 'User not created')

        user = {
            'type': 'admin',
            'first_name': 'modified_andrew',
            'last_name': 'modified_andrew',
            'username': 'andrew',
            'email': 'andrew@domain.com',
            'password': 'andrew'
        }
        response = self.app.put(
            self.path,
            headers=self.headers,
            data=json.dumps({'email': 'andrew@domain.com', 'data': user})
        )
        self.assertEqual(response.status_code, 200, 'User not updated')

        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'email': 'andrew@domain.com'})
        )
        self.assertEqual(response.status_code, 204, 'User not deleted')

    def test_delete_non_existent_user(self):
        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'email': 'ray@domain.com'})
        )
        self.assertEqual(response.status_code, 204, 'User not deleted')

    def test_get_user_by_name(self):
        user = {
            'type': 'admin',
            'first_name': 'sam',
            'last_name': 'sam',
            'username': 'sam',
            'email': 'sam@domain.com',
            'password': 'sam'
        }
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(user)
        )
        self.assertEqual(response.status_code, 200, 'User not created')

        response = self.app.get(
            self.path + '/' + user['username'],
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200, 'User not fetched')
        self.assertEqual(
            json.loads(response.data)['username'],
            user['username'],
            'Wrong username'
        )
        self.assertEqual(json.loads(response.data)['email'], user['email'],
                         'Wrong email')
        self.assertIsInstance(json.loads(response.data)['public_id'], str,
                              'Wrong public_id')

        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'email': 'sam@domain.com'})
        )
        self.assertEqual(response.status_code, 204, 'User not deleted')

    def test_query_users(self):
        user1 = {
            'type': 'admin',
            'first_name': 'violet',
            'last_name': 'violet',
            'username': 'violet',
            'email': 'violet@domain.com',
            'password': 'violet'
        }

        user2 = {
            'type': 'admin',
            'first_name': 'julia',
            'last_name': 'julia',
            'username': 'julia',
            'email': 'julia@domain.com',
            'password': 'julia'
        }

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(user1)
        )
        self.assertEqual(response.status_code, 200, 'User1 not created')

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(user2)
        )
        self.assertEqual(response.status_code, 200, 'User2 not created')

        response = self.app.post(
            self.path + '/query',
            headers=self.headers,
            data=json.dumps({
                'query': {
                    'type': 'admin'
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Users not found')
        self.assertGreaterEqual(json.loads(response.data)['total'], 2)

        response = self.app.post(
            self.path + '/query',
            headers=self.headers,
            data=json.dumps({
                'query': {},
                'filter': {
                    'username': 1
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Users not found')
        self.assertGreaterEqual(json.loads(response.data)['total'], 2)
        for user in json.loads(response.data)['items']:
            self.assertEqual(list(user.keys()), ['username'], 'Wrong keys')
