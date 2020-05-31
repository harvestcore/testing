import json
import unittest

from src.app import app
from src.classes.customer import Customer
from src.classes.user import User
from src.classes.login import Login

from tests.utils.auth import Auth

from config.server_environment import TESTING_DATABASE


class StatusServiceTests(unittest.TestCase):
    app = app.test_client()

    def test_status(self):
        Customer().set_customer(TESTING_DATABASE)
        User().insert({
            'type': 'admin',
            'first_name': 'status',
            'last_name': 'status',
            'username': 'status',
            'email': 'status',
            'password': 'status'
        })

        logged_user = Login().login(Auth('status', 'status'))
        self.headers = {
            'Content-Type': 'application/json',
            'x-access-token': logged_user.data['token']
        }

        response = self.app.get(
            '/api/status',
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200, 'Status not found')

        data = json.loads(response.data)
        keys = ['is_up', 'data_usage', 'info']

        self.assertEqual('docker' in data, True, 'Missing docker status')
        self.assertEqual('mongo' in data, True, 'Missing mongo status')

        for key in keys:
            self.assertEqual(key in data['docker'], True,
                             key + ' missing in docker status')
            self.assertEqual(key in data['mongo'], True,
                             key + ' missing in mongo status')

    def test_healthcheck(self):
        Customer().set_customer(TESTING_DATABASE)
        response = self.app.get('/api/healthcheck')

        self.assertEqual(response.status_code, 200, 'Healthcheck not found')

        data = json.loads(response.data)

        self.assertEqual('ok' in data, True, 'Missing healthcheck')
