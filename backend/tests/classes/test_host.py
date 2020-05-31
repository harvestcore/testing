import unittest

from src.classes.ansible.host import Host
from src.classes.customer import Customer
from src.classes.mongo_engine import MongoEngine

from config.server_environment import TESTING_DATABASE


class HostTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(HostTests, self).__init__(*args, **kwargs)

        # Drop previous database
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'hosts')

    def test_create_host(self):
        status = Host().insert({
            'name': 'host1',
            'ips': ['192.168.1.5', '192.168.2.5']
        })

        self.assertEqual(status, True, 'Host not added')

    def test_create_duplicated_host(self):
        Host().insert({
            'name': 'host1',
            'ips': ['192.168.1.5', '192.168.2.5']
        })

        status = Host().insert({
            'name': 'host1',
            'ips': ['192.168.1.5', '192.168.2.5']
        })

        self.assertEqual(status, False, 'Added duplicated host')

    def test_find_host(self):
        h = {
            'name': 'host1',
            'ips': ['192.168.1.5', '192.168.2.5']
        }
        keys = ['_id', 'name', 'ips', 'deleted']

        Host().insert(h)
        host = Host().find()

        self.assertNotEqual(host, None, 'Host obj not found')
        self.assertIsInstance(host.data, dict,
                              'Host data is not a dict')
        self.assertListEqual(list(host.data.keys()), keys,
                             'Keys are not equal')
        self.assertEqual(host.data['name'], h['name'], 'name not equal')
        self.assertEqual(host.data['ips'], h['ips'], 'ips not equal')

    def test_find_all_hosts(self):
        Host().insert({
            'name': 'host1',
            'ips': ['192.168.1.2', '192.168.2.3']
        })

        Host().insert({
            'name': 'host2',
            'ips': ['192.168.1.4', '192.168.2.5']
        })

        hosts = Host().find()

        self.assertIsInstance(hosts.data, list,
                              'Hosts data is not a list')
        self.assertEqual(len(hosts.data), 2, 'There are more than 2 hosts')
