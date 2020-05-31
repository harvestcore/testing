import json
import unittest

from src.app import app
from src.classes.customer import Customer
from src.classes.machine import Machine
from src.classes.mongo_engine import MongoEngine

from tests.utils.login import TestingLogin

from config.server_environment import TESTING_DATABASE


class UserTests(unittest.TestCase):
    app = app.test_client()
    headers = TestingLogin().headers
    path = '/api/machine'

    def setUp(self):
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'machines')

    def test_create_full_machine(self):
        machine = {
            'name': 'machine1',
            'description': 'cool machine1',
            'type': 'local',
            'ipv4': '192.168.1.10',
            'ipv6': 'fdf8:f53b:82e4::53',
            'mac': '00:0a:95:9d:68:16',
            'broadcast': '192.168.1.255',
            'gateway': '192.168.1.1',
            'netmask': '255.255.255.0',
            'network': '192.168.1.0'
        }

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(machine)
        )
        self.assertEqual(response.status_code, 200,
                         'Machine (local) not added')

        machine = {
            'name': 'machine2',
            'description': 'cool machine2',
            'type': 'remote',
            'ipv4': '192.168.1.10',
            'ipv6': 'fdf8:f53b:82e4::53',
            'mac': '00:0a:95:9d:68:16',
            'broadcast': '192.168.1.255',
            'gateway': '192.168.1.1',
            'netmask': '255.255.255.0',
            'network': '192.168.1.0'
        }

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(machine)
        )
        self.assertEqual(response.status_code, 200,
                         'Machine (remote) not added')

    def create_empty_machine(self):
        machine = {
            'name': 'machine3',
            'type': 'local'
        }

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(machine)
        )
        self.assertEqual(response.status_code, 200,
                         'Machine not added')

    def test_create_duplicated_customer(self):
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps({
                'name': 'machine4',
                'type': 'local'
            })
        )
        self.assertEqual(response.status_code, 200,
                         'Machine not added')

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps({
                'name': 'machine4',
                'type': 'local'
            })
        )

        self.assertEqual(response.status_code, 422,
                         'Duplicated machine added')

    def create_machine_with_missing_info(self):
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps({
                'name': 'machine5',
                'description': 'cool machine5',
                'type': 'remote',
                'ipv4': '192.168.1.10',
                'broadcast': '192.168.1.255',
                'network': '192.168.1.0'
            })
        )
        self.assertEqual(response.status_code, 200, 'Machine not added')

    def create_machine_with_wrong_ip(self):
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps({
                'name': 'machine6',
                'description': 'cool machine6',
                'type': 'remote',
                'ipv4': '192.168.1.500',
                'broadcast': '192.168.1.255',
                'network': '192.168.1.0'
            })
        )
        self.assertEqual(response.status_code, 422,
                         'Machine with wrong ipv4 added')

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps({
                'name': 'machine7',
                'description': 'cool machine7',
                'type': 'remote',
                'ipv6': '192.168.1.500',
                'broadcast': '192.168.1.255',
                'network': '192.168.1.0'
            })
        )
        self.assertEqual(response.status_code, 422,
                         'Machine with wrong ipv6 added')

    def create_machine_with_wrong_mac(self):
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps({
                'name': 'machine8',
                'description': 'cool machine8',
                'type': 'remote',
                'ipv4': '192.168.1.10',
                'mac': '00:0a:95:9d',
                'broadcast': '192.168.1.255',
                'network': '192.168.1.0'
            })
        )
        self.assertEqual(response.status_code, 422,
                         'Machine with wrong ipv4 added')

    def test_find_full_machine(self):
        m = {
            'name': 'machine9',
            'description': 'cool machine9',
            'type': 'remote',
            'ipv4': '192.168.1.10',
            'ipv6': 'fdf8:f53b:82e4::53',
            'mac': '00:0a:95:9d:68:16',
            'broadcast': '192.168.1.255',
            'gateway': '192.168.1.1',
            'netmask': '255.255.255.0',
            'network': '192.168.1.0'
        }

        Machine().insert(m)

        response = self.app.get(
            self.path + '/' + m['name'],
            headers=self.headers
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200, 'Machine not found')
        self.assertIsInstance(data, dict, 'Machine data is not a dict')

        self.assertEqual(m['name'], data['name'], 'Wrong name')
        self.assertEqual(m['description'], data['description'],
                         'Wrong description')
        self.assertEqual(m['gateway'], data['gateway'], 'Wrong gateway')
        self.assertEqual(m['mac'], data['mac'], 'Wrong mac')

    def test_find_all_machines(self):
        Machine().insert({
            'name': 'machine10',
            'description': 'cool machine10',
            'type': 'remote',
            'ipv4': '192.168.1.10',
            'ipv6': 'fdf8:f53b:82e4::53',
            'mac': '00:0a:95:9d:68:16',
            'broadcast': '192.168.1.255',
            'gateway': '192.168.1.1',
            'netmask': '255.255.255.0',
            'network': '192.168.1.0'
        })

        Machine().insert({
            'name': 'machine11',
            'description': 'cool machine11',
            'type': 'remote',
            'ipv4': '192.168.1.10',
            'ipv6': 'fdf8:f53b:82e4::53',
            'mac': '00:0a:95:9d:68:16',
            'broadcast': '192.168.1.255',
            'gateway': '192.168.1.1',
            'netmask': '255.255.255.0',
            'network': '192.168.1.0'
        })

        response = self.app.post(
            self.path + '/query',
            headers=self.headers,
            data=json.dumps({
                'query': {}
            })
        )
        self.assertEqual(response.status_code, 200, 'Machines not found')
        self.assertEqual(json.loads(response.data)['total'], 2)

    def test_update_machine(self):
        m = {
            'name': 'machine12',
            'description': 'cool machine12',
            'type': 'remote',
            'ipv4': '192.168.1.10',
            'ipv6': 'fdf8:f53b:82e4::53',
            'mac': '00:0a:95:9d:68:16',
            'broadcast': '192.168.1.255',
            'gateway': '192.168.1.1',
            'netmask': '255.255.255.0',
            'network': '192.168.1.0'
        }

        Machine().insert(m)

        response = self.app.put(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': m['name'], 'data': {
                    'name': 'machine12',
                    'description': 'TEST machine',
                    'type': 'local',
                    'ipv4': '10.0.0.10',
                    'ipv6': 'fdf8:f53b:82e4::53',
                    'mac': '00:0a:95:9d:68:16',
                    'broadcast': '192.168.1.255',
                    'gateway': '192.168.1.1',
                    'netmask': '255.255.255.0',
                    'network': '10.0.0.0'
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Machine not updated')

        machine = Machine().find({'name': m['name']})

        self.assertIsInstance(machine.data, dict, 'Machine data is not a dict')
        self.assertEqual(machine.data['network'], '10.0.0.0', 'Wrong network')
        self.assertEqual(machine.data['description'], 'TEST machine',
                         'Wrong description')

    def test_remove_machine(self):
        m = {
            'name': 'machine13',
            'description': 'cool machine13',
            'type': 'remote',
            'ipv4': '192.168.1.10',
            'ipv6': 'fdf8:f53b:82e4::53',
            'mac': '00:0a:95:9d:68:16',
            'broadcast': '192.168.1.255',
            'gateway': '192.168.1.1',
            'netmask': '255.255.255.0',
            'network': '192.168.1.0'
        }

        Machine().insert(m)
        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': m['name']})
        )
        self.assertEqual(response.status_code, 204, 'Machine not deleted')
