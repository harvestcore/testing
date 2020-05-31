import json
import unittest

from src.app import app
from src.classes.customer import Customer
from src.classes.mongo_engine import MongoEngine
from src.classes.login import Login
from src.classes.user import User

from tests.utils.auth import Auth

from config.server_environment import TESTING_DATABASE


class CustomerServiceTests(unittest.TestCase):
    app = app.test_client()
    path = '/api/customer'

    def setUp(self):
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'customers')
        User().insert({
            'type': 'admin',
            'first_name': 'admin-user',
            'last_name': 'admin-user',
            'username': 'admin-user',
            'email': 'admin-user',
            'password': 'admin-user'
        })

        logged_user = Login().login(Auth('admin-user', 'admin-user'))
        self.headers = {
            'Content-Type': 'application/json',
            'x-access-token': logged_user.data['token']
        }

    def test_create_and_delete_customer(self):
        customer = {
            'domain': 'test-customer',
            'db_name': 'test-customer'
        }

        Customer().remove(customer)

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(customer)
        )
        self.assertEqual(response.status_code, 200, 'Customer not created')

        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'domain': 'test-customer'})
        )
        self.assertEqual(response.status_code, 204, 'User not deleted')

    def test_update_customer(self):
        customer = {
            'domain': 'test-customer2',
            'db_name': 'test-customer2'
        }

        Customer().insert(customer)

        customer = {
            'domain': 'test-c2',
            'db_name': 'test-c2',
            'enabled': True
        }
        response = self.app.put(
            self.path,
            headers=self.headers,
            data=json.dumps({'domain': 'test-customer2', 'data': customer})
        )
        self.assertEqual(response.status_code, 200, 'Customer not updated')

    def test_delete_non_existent_customer(self):
        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'domain': 'non-existing-domain'})
        )
        self.assertEqual(response.status_code, 204, 'Customer not deleted')

    def test_query_users(self):
        c1 = {
            'domain': 'test-customer3',
            'db_name': 'test-customer3'
        }

        c2 = {
            'domain': 'test-customer4',
            'db_name': 'test-customer4'
        }

        Customer().insert(c1)
        Customer().insert(c2)

        response = self.app.post(
            self.path + '/query',
            headers=self.headers,
            data=json.dumps({
                'query': {
                    'enabled': True
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Customers not found')
        self.assertGreaterEqual(json.loads(response.data)['total'], 2)

        response = self.app.post(
            self.path + '/query',
            headers=self.headers,
            data=json.dumps({
                'query': {},
                'filter': {
                    'domain': 1
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Customers not found')
        self.assertGreaterEqual(json.loads(response.data)['total'], 2)
        for user in json.loads(response.data)['items']:
            self.assertEqual(list(user.keys()), ['domain'], 'Wrong keys')
