import json
import unittest

from src.app import app
from src.classes.customer import Customer
from src.classes.user import User

from tests.utils.login import TestingLogin

from config.server_environment import TESTING_DATABASE


class LoginServiceTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.headers = TestingLogin().headers

    def test_login_and_logout(self):
        Customer().set_customer(TESTING_DATABASE)
        User().insert({
            'type': 'admin',
            'first_name': 'usertest',
            'last_name': 'usertest',
            'username': 'usertest',
            'email': 'usertest@domain.com',
            'password': 'usertest'
        })

        response = self.app.get(
            '/api/login',
            headers={"Authorization": "Basic dXNlcnRlc3Q6dXNlcnRlc3Q="}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertNotEqual(data, "", 'There is no token')
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': data['token']
        }

        response = self.app.get(
            '/api/logout',
            headers=headers
        )
        self.assertEqual(response.status_code, 200, 'Logout failed')
