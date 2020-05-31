import json
import unittest

from src.app import app
from src.classes.customer import Customer
from src.classes.mongo_engine import MongoEngine
from src.classes.docker_engine import DockerEngine
from src.classes.ansible.host import Host
from src.classes.ansible.playbook import Playbook

from tests.utils.login import TestingLogin

from config.server_environment import TESTING_DATABASE


class ProvisionHostServiceTests(unittest.TestCase):
    path = '/api/provision/hosts'
    app = app.test_client()
    headers = TestingLogin().headers

    def setUp(self):
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'hosts')
        MongoEngine().drop_collection(TESTING_DATABASE, 'playbooks')

    def test_create_host(self):
        host = {
            'name': 'benjamin',
            'ips': ['10.10.10.10']
        }
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(host)
        )
        self.assertEqual(response.status_code, 200, 'Host not created')

        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': 'benjamin'})
        )
        self.assertEqual(response.status_code, 204, 'Host not deleted')

    def test_update_host(self):
        host = {
            'name': 'harry',
            'ips': ['10.10.10.10']
        }
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(host)
        )
        self.assertEqual(response.status_code, 200, 'Host not created')

        host = {
            'name': 'harry',
            'ips': ['10.10.10.10', '20.20.20.20']
        }
        response = self.app.put(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': 'harry', 'data': host})
        )
        self.assertEqual(response.status_code, 200, 'Host not updated')

        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': 'harry'})
        )
        self.assertEqual(response.status_code, 204, 'Host not deleted')

    def test_delete_non_existent_host(self):
        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': 'fernando'})
        )
        self.assertEqual(response.status_code, 204, 'Host not deleted')

    def test_get_host_by_name(self):
        host = {
            'name': 'lucas',
            'ips': ['10.10.10.10']
        }
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(host)
        )
        self.assertEqual(response.status_code, 200, 'Host not created')

        response = self.app.get(
            self.path + '/' + host['name'],
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200, 'Host not fetched')
        self.assertEqual(json.loads(response.data)['name'], host['name'],
                         'Wrong name')
        self.assertEqual(json.loads(response.data)['ips'], host['ips'],
                         'Wrong ips')

        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': 'lucas'})
        )
        self.assertEqual(response.status_code, 204, 'Host not deleted')

    def test_query_hosts(self):
        host1 = {
            'name': 'margarita',
            'ips': ['10.10.10.10']
        }

        host2 = {
            'name': 'vera',
            'ips': ['10.10.10.10']
        }

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(host1)
        )
        self.assertEqual(response.status_code, 200, 'Host1 not created')

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(host2)
        )
        self.assertEqual(response.status_code, 200, 'Host2 not created')

        response = self.app.post(
            self.path + '/query',
            headers=self.headers,
            data=json.dumps({
                'query': {}
            })
        )
        self.assertEqual(response.status_code, 200, 'Hosts not found')
        self.assertGreaterEqual(json.loads(response.data)['total'], 2,
                                'Too many hosts')

        response = self.app.post(
            self.path + '/query',
            headers=self.headers,
            data=json.dumps({
                'query': {},
                'filter': {
                    'ips': 1
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Hosts not found')
        self.assertGreaterEqual(
            json.loads(response.data)['total'], 2,
            'Too many hosts'
        )
        for user in json.loads(response.data)['items']:
            self.assertEqual(list(user.keys()), ['ips'], 'Wrong keys')


class ProvisionPlaybookServiceTests(unittest.TestCase):
    app = app.test_client()
    headers = TestingLogin().headers
    path = '/api/provision/playbook'

    def setUp(self):
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'playbooks')

    def test_create_playbook(self):
        playbook = {
            'name': 'arthur',
            'playbook': {
                'hosts': 'arthur',
                'remote_user': 'arthur',
                'tasks': [
                    {
                        'name': 'test debug',
                        'debug': {
                            'msg': 'Debug msg'
                        }
                    }
                ]
            }
        }
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(playbook)
        )
        self.assertEqual(response.status_code, 200, 'Playbook not created')

        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': 'arthur'})
        )
        self.assertEqual(response.status_code, 204, 'Playbook not deleted')

    def test_update_playbook(self):
        playbook = {
            'name': 'arthur',
            'playbook': {
                'hosts': 'arthur',
                'remote_user': 'arthur',
                'tasks': [
                    {
                        'name': 'test debug',
                        'debug': {
                            'msg': 'Debug msg'
                        }
                    }
                ]
            }
        }
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(playbook)
        )
        self.assertEqual(response.status_code, 200, 'Playbook not created')

        playbook = {
            'name': 'arthur',
            'playbook': {
                'hosts': 'modified_arthur',
                'remote_user': 'modified_arthur',
                'tasks': [
                    {
                        'name': 'test debug',
                        'debug': {
                            'msg': 'Debug msg'
                        }
                    }
                ]
            }
        }
        response = self.app.put(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': 'arthur', 'data': playbook})
        )
        self.assertEqual(response.status_code, 200, 'Playbook not updated')

        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': 'arthur'})
        )
        self.assertEqual(response.status_code, 204, 'Playbook not deleted')

    def test_delete_non_existent_playbook(self):
        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': 'frank'})
        )
        self.assertEqual(response.status_code, 204, 'Playbook not deleted')

    def test_get_playbook_by_name(self):
        playbook = {
            'name': 'lewis',
            'playbook': {
                'hosts': 'lewis',
                'remote_user': 'lewis',
                'tasks': [
                    {
                        'name': 'test debug',
                        'debug': {
                            'msg': 'Debug msg'
                        }
                    }
                ]
            }
        }
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(playbook)
        )
        self.assertEqual(response.status_code, 200, 'Playbook not created')

        response = self.app.get(
            self.path + '/' + playbook['name'],
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200, 'Playbook not fetched')
        self.assertEqual(json.loads(response.data)['name'], playbook['name'],
                         'Wrong name')
        self.assertEqual(
            json.loads(response.data)['playbook'][0],
            playbook['playbook'],
            'Wrong playbook'
        )

        response = self.app.delete(
            self.path,
            headers=self.headers,
            data=json.dumps({'name': 'lewis'})
        )
        self.assertEqual(response.status_code, 204, 'Playbook not deleted')

    def test_query_playbooks(self):
        playbook1 = {
            'name': 'agnes',
            'playbook': {
                'hosts': 'agnes',
                'remote_user': 'agnes',
                'tasks': [
                    {
                        'name': 'test debug',
                        'debug': {
                            'msg': 'Debug msg'
                        }
                    }
                ]
            }
        }

        playbook2 = {
            'name': 'betty',
            'playbook': {
                'hosts': 'betty',
                'remote_user': 'betty',
                'tasks': [
                    {
                        'name': 'test debug',
                        'debug': {
                            'msg': 'Debug msg'
                        }
                    }
                ]
            }
        }

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(playbook1)
        )
        self.assertEqual(response.status_code, 200, 'Playbook1 not created')

        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps(playbook2)
        )
        self.assertEqual(response.status_code, 200, 'Playbook2 not created')

        response = self.app.post(
            self.path + '/query',
            headers=self.headers,
            data=json.dumps({
                'query': {}
            })
        )
        self.assertEqual(response.status_code, 200, 'Playbooks not found')
        self.assertGreaterEqual(json.loads(response.data)['total'], 2)

        response = self.app.post(
            self.path + '/query',
            headers=self.headers,
            data=json.dumps({
                'query': {},
                'filter': {
                    'playbook': 1
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Playbooks not found')
        self.assertGreaterEqual(json.loads(response.data)['total'], 2)
        for user in json.loads(response.data)['items']:
            self.assertEqual(list(user.keys()), ['playbook'], 'Wrong keys')


class ProvisionRunPlaybooksServiceTests(unittest.TestCase):
    app = app.test_client()
    headers = TestingLogin().headers
    path = '/api/provision'
    playbook = 'test-alpine-ssh'
    hosts = ['alpine']

    def setUp(self):
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'hosts')
        MongoEngine().drop_collection(TESTING_DATABASE, 'playbooks')

    def test_run_playbook(self):
        ips = '172.17.0.'

        response_list = DockerEngine().run_container_operation(
            operation='list',
            data={
                'all': False
            }
        )

        if len(response_list) > 0:
            ips = ips + str(2 + len(response_list))
        else:
            ips = ips + '2'

        h = Host().insert({
            'name': self.hosts[0],
            'ips': ips
        })

        self.assertEqual(h, True, 'Host not added')

        p = Playbook().insert({
            'name': self.playbook,
            'playbook': {
                'hosts': self.hosts[0],
                'remote_user': 'root',
                'tasks': [
                    {
                        'name': 'Test debug msg',
                        'debug': {
                            'msg': 'This works!'
                        }
                    }
                ]
            }
        })

        self.assertEqual(p, True, 'Playbook not added')

        container = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'sickp/alpine-sshd',
                'detach': True
            }
        )

        self.assertNotEqual(container, False, 'Cointainer not running')
        self.container_id = container.short_id

        # Run the playbook
        response = self.app.post(
            self.path,
            headers=self.headers,
            data=json.dumps({
                'hosts': self.hosts,
                'playbook': self.playbook,
                'passwords': {
                    'conn_pass': 'root',
                    'become_pass': 'root'
                }
            })
        )

        self.assertEqual(response.status_code, 200, 'Playbook failed running')
        self.assertNotEqual(json.loads(response.data)['result']
                            .find('PLAY [alpine]'), -1)

        # Stop the container
        c = DockerEngine().get_container_by_id(self.container_id)
        DockerEngine().run_operation_in_object(
            object=c,
            operation='stop',
            data={}
        )
