import json
import unittest

from src.app import app
from src.classes.customer import Customer

from tests.utils.login import TestingLogin

from config.server_environment import TESTING_DATABASE


class DeployContainerServiceTests(unittest.TestCase):
    app = app.test_client()
    headers = TestingLogin().headers
    path = '/api/deploy'

    def setUp(self):
        Customer().set_customer(TESTING_DATABASE)

    def test_run_hello_world_container(self):
        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'hello-world'
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Image run failed')

    def test_run_and_stop_background_container(self):
        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'mongo:4.2.3',
                    'detach': True
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Container not run')
        self.assertEqual(json.loads(response.data)['status'], 'created',
                         'Container not created')

        short_id = json.loads(response.data)['short_id']

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'stop',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not stopped')

    def test_get_running_container(self):
        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'mongo:4.2.3',
                    'detach': True
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Container not run')
        self.assertEqual(json.loads(response.data)['status'], 'created',
                         'Container not created')

        short_id = json.loads(response.data)['short_id']

        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'get',
                'data': {
                    'container_id': short_id
                }
            })
        )

        self.assertEqual(response.status_code, 200,
                         'Container info not fetched')
        self.assertEqual(json.loads(response.data)['short_id'], short_id,
                         'Wrong container')

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'stop',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not stopped')

    def test_list_running_containers(self):
        response1 = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'mongo:4.2.3',
                    'detach': True
                }
            })
        )
        self.assertEqual(response1.status_code, 200, 'Container not run')
        self.assertEqual(json.loads(response1.data)['status'], 'created',
                         'Container not created')

        response2 = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'mongo:4.2.3',
                    'detach': True
                }
            })
        )
        self.assertEqual(response2.status_code, 200, 'Container not run')
        self.assertEqual(json.loads(response2.data)['status'], 'created',
                         'Container not created')

        short_id_1 = json.loads(response1.data)['short_id']
        short_id_2 = json.loads(response2.data)['short_id']

        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'list',
                'data': {
                    'all': False
                }
            })
        )

        self.assertEqual(response.status_code, 200,
                         'Container list not fetched')
        self.assertGreaterEqual(json.loads(response.data)['total'], 2,
                                'Wrong container number')

        response1 = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id_1,
                'operation': 'stop',
                'data': {}
            })
        )

        response2 = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id_2,
                'operation': 'stop',
                'data': {}
            })
        )

        self.assertEqual(response1.status_code, 200, 'Container1 not stopped')
        self.assertEqual(response2.status_code, 200, 'Container2 not stopped')

    def test_prune_containers(self):
        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'prune',
                'data': {}
            })
        )
        self.assertEqual(response.status_code, 200, 'Containers not pruned')
        self.assertEqual(json.loads(response.data), {},
                         'Containers not pruned')

    def test_kill_container(self):
        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'mongo:4.2.3',
                    'detach': True
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Container not run')
        self.assertEqual(json.loads(response.data)['status'], 'created',
                         'Container not created')

        short_id = json.loads(response.data)['short_id']

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'kill',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not killed')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not killed')

    def test_logs_container(self):
        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'mongo:4.2.3',
                    'detach': True
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Container not run')
        self.assertEqual(json.loads(response.data)['status'], 'created',
                         'Container not created')

        short_id = json.loads(response.data)['short_id']

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'logs',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not stopped')
        self.assertIsInstance(json.loads(response.data)['data'], str,
                              'Wrong container logs')

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'stop',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not stopped')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not stopped')

    def test_pause_unpause_container(self):
        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'mongo:4.2.3',
                    'detach': True
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Container not run')
        self.assertEqual(json.loads(response.data)['status'], 'created',
                         'Container not created')

        short_id = json.loads(response.data)['short_id']

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'pause',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not paused')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not stopped')

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'unpause',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not unpaused')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not stopped')

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'stop',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not stopped')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not stopped')

    def test_reload_container(self):
        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'mongo:4.2.3',
                    'detach': True
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Container not run')
        self.assertEqual(json.loads(response.data)['status'], 'created',
                         'Container not created')

        short_id = json.loads(response.data)['short_id']

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'reload',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not reloaded')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not reloaded')

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'stop',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not stopped')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not stopped')

    def test_rename_container(self):
        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'mongo:4.2.3',
                    'detach': True
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Container not run')
        self.assertEqual(json.loads(response.data)['status'], 'created',
                         'Container not created')

        short_id = json.loads(response.data)['short_id']

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'rename',
                'data': {
                    'name': 'testing-name'
                }
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not renamed')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not renamed')

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'stop',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not stopped')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not stopped')

    def test_rename_container(self):
        response = self.app.post(
            self.path + '/container',
            headers=self.headers,
            data=json.dumps({
                'operation': 'run',
                'data': {
                    'image': 'mongo:4.2.3',
                    'detach': True
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Container not run')
        self.assertEqual(json.loads(response.data)['status'], 'created',
                         'Container not created')

        short_id = json.loads(response.data)['short_id']

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'restart',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not restarted')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not restarted')

        response = self.app.post(
            self.path + '/container/single',
            headers=self.headers,
            data=json.dumps({
                'container_id': short_id,
                'operation': 'stop',
                'data': {}
            })
        )

        self.assertEqual(response.status_code, 200, 'Container not stopped')
        self.assertEqual(json.loads(response.data)['data'], None,
                         'Container not stopped')
