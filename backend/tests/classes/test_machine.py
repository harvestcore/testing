import unittest

from src.classes.machine import Machine
from src.classes.customer import Customer
from src.classes.mongo_engine import MongoEngine

from config.server_environment import TESTING_DATABASE


class UserTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(UserTests, self).__init__(*args, **kwargs)

        # Drop previous database
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'machines')

    def test_create_full_machine(self):
        status = Machine().insert({
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
        })
        self.assertEqual(status, True, 'Machine (local) not added')

        status = Machine().insert({
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
        })
        self.assertEqual(status, True, 'Machine (remote) not added')

    def create_empty_machine(self):
        status = Machine().insert({
            'name': 'machine3',
            'type': 'local'
        })
        self.assertEqual(status, True, 'Machine not added')

    def test_create_duplicated_customer(self):
        Machine().insert({
            'name': 'machine4',
            'type': 'local'
        })

        status = Machine().insert({
            'name': 'machine4',
            'type': 'local'
        })
        self.assertEqual(status, False, 'Duplicated machine added')

    def create_machine_with_missing_info(self):
        status = Machine().insert({
            'name': 'machine5',
            'description': 'cool machine5',
            'type': 'remote',
            'ipv4': '192.168.1.10',
            'broadcast': '192.168.1.255',
            'network': '192.168.1.0'
        })
        self.assertEqual(status, True, 'Machine not added')

    def create_machine_with_wrong_ip(self):
        status = Machine().insert({
            'name': 'machine6',
            'description': 'cool machine6',
            'type': 'remote',
            'ipv4': '192.168.1.500',
            'broadcast': '192.168.1.255',
            'network': '192.168.1.0'
        })
        self.assertEqual(status, False, 'Machine with wrong ipv4 added')

        status = Machine().insert({
            'name': 'machine7',
            'description': 'cool machine7',
            'type': 'remote',
            'ipv6': '192.168.1.500',
            'broadcast': '192.168.1.255',
            'network': '192.168.1.0'
        })
        self.assertEqual(status, False, 'Machine with wrong ipv6 added')

    def create_machine_with_wrong_mac(self):
        status = Machine().insert({
            'name': 'machine8',
            'description': 'cool machine8',
            'type': 'remote',
            'ipv4': '192.168.1.10',
            'mac': '00:0a:95:9d',
            'broadcast': '192.168.1.255',
            'network': '192.168.1.0'
        })
        self.assertEqual(status, False, 'Machine with wrong mac added')

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

        keys = ['_id', 'name', 'description', 'type', 'ipv4', 'ipv6', 'mac',
                'broadcast', 'gateway', 'netmask', 'network', 'deleted']

        Machine().insert(m)
        machine = Machine().find({'name': m['name']})

        self.assertNotEqual(machine, None, 'Machine not created')
        self.assertIsInstance(machine.data, dict, 'Machine data is not a dict')
        self.assertListEqual(list(machine.data.keys()), keys,
                             'Keys are not equal')

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

        machines = Machine().find()

        self.assertIsInstance(machines.data, list,
                              'Machines data is not a list')
        self.assertEqual(len(machines.data), 2,
                         'There are more than 2 machines')

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

        m['description'] = 'TEST'
        m['network'] = '10.0.0.0'

        status = Machine().update({'name': m['name']}, m)
        machine = Machine().find({'name': m['name']})

        self.assertNotEqual(status, False, 'Machine not updated')

        self.assertIsInstance(machine.data, dict, 'Machine data is not a dict')
        self.assertEqual(machine.data['network'], '10.0.0.0', 'Wrong network')
        self.assertEqual(machine.data['description'], 'TEST',
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
        status = Machine().remove({'name': m['name']})
        self.assertEqual(status, True, 'Machine not deleted')
