import unittest
from cryptography.fernet import Fernet

from src.classes.user import User
from src.classes.customer import Customer
from src.classes.mongo_engine import MongoEngine

from config.server_environment import TESTING_DATABASE, ENC_KEY


class UserTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(UserTests, self).__init__(*args, **kwargs)

        # Drop previous database
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'users')

    def test_create_users(self):
        status = User().insert({
            'type': 'admin',
            'first_name': 'Admin',
            'last_name': '1',
            'username': 'admin1',
            'email': 'admin1@domain.com',
            'password': 'admin1'
        })
        self.assertEqual(status, True, 'User (admin) not added')

        status2 = User().insert({
            'type': 'regular',
            'first_name': 'User',
            'last_name': '1',
            'username': 'user1',
            'email': 'user1@domain.com',
            'password': 'user1'
        })
        self.assertEqual(status2, True, 'User (regular) not added')

    def test_create_duplicated_customer(self):
        User().insert({
            'type': 'admin',
            'first_name': 'Admin',
            'last_name': '1',
            'username': 'admin1',
            'email': 'admin1@domain.com',
            'password': 'admin1'
        })

        status = User().insert({
            'type': 'admin',
            'first_name': 'Admin',
            'last_name': '1',
            'username': 'admin1',
            'email': 'admin1@domain.com',
            'password': 'admin1'
        })

        self.assertEqual(status, False, 'Added duplicated user')

    def test_find_user(self):
        u = {
            'type': 'admin',
            'first_name': 'Admin',
            'last_name': '1',
            'username': 'admin1',
            'email': 'admin1@domain.com',
            'password': 'admin1'
        }
        keys = ['_id', 'type', 'first_name', 'last_name', 'username', 'email',
                'password', 'enabled', 'deleted', 'public_id']
        User().insert(u)
        user = User().find()

        self.assertNotEqual(user, None, 'User obj not created')
        self.assertIsInstance(user.data, dict,
                              'User data is not a dict')
        self.assertListEqual(list(user.data.keys()), keys,
                             'Keys are not equal')
        self.assertEqual(user.data['type'], u['type'], 'Type not equal')
        self.assertEqual(user.data['first_name'], u['first_name'],
                         'first_name not equal')
        self.assertEqual(user.data['last_name'], u['last_name'],
                         'last_name not equal')
        self.assertEqual(user.data['username'], u['username'],
                         'username not equal')
        self.assertEqual(user.data['email'], u['email'], 'email not equal')

    def test_find_all_users(self):
        User().insert({
            'type': 'admin',
            'first_name': 'Admin',
            'last_name': '1',
            'username': 'admin1',
            'email': 'admin1@domain.com',
            'password': 'admin1'
        })

        User().insert({
            'type': 'regular',
            'first_name': 'User',
            'last_name': '1',
            'username': 'user1',
            'email': 'user1@domain.com',
            'password': 'user1'
        })

        users = User().find()

        self.assertIsInstance(users.data, list,
                              'User data is not a list')
        self.assertEqual(len(users.data), 2, 'There are more than 2 users')

    def test_password_is_encrypted(self):
        User().insert({
            'type': 'admin',
            'first_name': 'Admin',
            'last_name': '1',
            'username': 'admin1',
            'email': 'admin1@domain.com',
            'password': 'admin1'
        })

        f = Fernet(ENC_KEY)

        user = User().find({'username': 'admin1'})

        self.assertNotEqual(f.decrypt(user.data['password'].encode()),
                            'admin1', 'Pass not encrypted')
        self.assertEqual(f.decrypt(user.data['password'].encode()).decode(),
                         'admin1', 'Pass decryption gone wrong')
