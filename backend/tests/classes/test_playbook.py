import unittest

from src.classes.ansible.playbook import Playbook
from src.classes.customer import Customer
from src.classes.mongo_engine import MongoEngine

from config.server_environment import TESTING_DATABASE


class PlaybookTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PlaybookTests, self).__init__(*args, **kwargs)

        # Drop previous database
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'playbooks')

    def test_create_playbook(self):
        status = Playbook().insert({
            'name': 'cool-playbook',
            'playbook': [
                {
                    'hosts': 'test',
                    'remote_user': 'test1',
                    'tasks': [
                        {
                            'name': 'test debug',
                            'debug': {
                                'msg': 'Debug msg'
                            }
                        }
                    ]
                }
            ]
        })

        self.assertEqual(status, True, 'Playbook not added')

    def test_create_duplicated_host(self):
        pb = {
            'name': 'cool-playbook',
            'playbook': [
                {
                    'hosts': 'test',
                    'remote_user': 'test1',
                    'tasks': [
                        {
                            'name': 'test debug',
                            'debug': {
                                'msg': 'Debug msg'
                            }
                        }
                    ]
                }
            ]
        }

        Playbook().insert(pb)
        status = Playbook().insert(pb)

        self.assertEqual(status, False, 'Added duplicated playbook')

    def test_find_playbook(self):
        h = {
            'name': 'cool-playbook',
            'playbook': [
                {
                    'hosts': 'test',
                    'remote_user': 'test1',
                    'tasks': [
                        {
                            'name': 'test debug',
                            'debug': {
                                'msg': 'Debug msg'
                            }
                        }
                    ]
                }
            ]
        }
        keys = ['_id', 'name', 'playbook', 'deleted']

        Playbook().insert(h)
        playbook = Playbook().find()

        self.assertNotEqual(playbook, None, 'Playbook obj not found')
        self.assertIsInstance(playbook.data, dict,
                              'Playbook data is not a dict')
        self.assertListEqual(list(playbook.data.keys()), keys,
                             'Keys are not equal')
        self.assertEqual(playbook.data['name'], h['name'], 'name not equal')
        self.assertEqual(playbook.data['playbook'], h['playbook'],
                         'playbook not equal')

    def test_find_all_hosts(self):
        Playbook().insert({
            'name': 'cool-playbook-1',
            'playbook': [
                {
                    'hosts': 'test',
                    'remote_user': 'test1',
                    'tasks': [
                        {
                            'name': 'test debug',
                            'debug': {
                                'msg': 'Debug msg'
                            }
                        }
                    ]
                }
            ]
        })

        Playbook().insert({
            'name': 'cool-playbook-2',
            'playbook': [
                {
                    'hosts': 'test',
                    'remote_user': 'test1',
                    'tasks': [
                        {
                            'name': 'test debug',
                            'debug': {
                                'msg': 'Debug msg'
                            }
                        }
                    ]
                }
            ]
        })

        playbooks = Playbook().find()

        self.assertIsInstance(playbooks.data, list,
                              'Hosts data is not a list')
        self.assertEqual(len(playbooks.data), 2,
                         'There are more than 2 playbooks')
