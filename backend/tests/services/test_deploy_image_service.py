import json
import unittest

from src.app import app
from src.classes.customer import Customer

from tests.utils.login import TestingLogin

from config.server_environment import TESTING_DATABASE


class DeployImageServiceTests(unittest.TestCase):
    app = app.test_client()
    headers = TestingLogin().headers
    path = '/api/deploy'

    def setUp(self):
        Customer().set_customer(TESTING_DATABASE)

    def test_pull_and_remove_image(self):
        response = self.app.post(
            self.path + '/image',
            headers=self.headers,
            data=json.dumps({
                'operation': 'pull',
                'data': {
                    'repository': 'alpine:latest'
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Image not pulled')

        response = self.app.post(
            self.path + '/image',
            headers=self.headers,
            data=json.dumps({
                'operation': 'remove',
                'data': {
                    'image': 'alpine',
                    'force': True
                }
            })
        )
        self.assertIn(response.status_code, [200, 422], 'Image not removed')

    def test_get_image(self):
        response = self.app.post(
            self.path + '/image',
            headers=self.headers,
            data=json.dumps({
                'operation': 'pull',
                'data': {
                    'repository': 'alpine:latest'
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Image not pulled')
        short_id = json.loads(response.data)['short_id']

        response = self.app.post(
            self.path + '/image',
            headers=self.headers,
            data=json.dumps({
                'operation': 'get',
                'data': {
                    'name': 'alpine'
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Image not fetched')
        self.assertEqual(json.loads(response.data)['short_id'], short_id,
                         'Image not fetched')

        response = self.app.post(
            self.path + '/image',
            headers=self.headers,
            data=json.dumps({
                'operation': 'remove',
                'data': {
                    'image': 'alpine',
                    'force': True
                }
            })
        )
        self.assertIn(response.status_code, [200, 422], 'Image not removed')

    def test_prune_images(self):
        response = self.app.post(
            self.path + '/image',
            headers=self.headers,
            data=json.dumps({
                'operation': 'prune',
                'data': {
                    'filters': {
                        'dangling': True
                    }
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Images not pruned')
        self.assertEqual(json.loads(response.data), {}, 'Images not pruned')

    def test_search_image(self):
        response = self.app.post(
            self.path + '/image',
            headers=self.headers,
            data=json.dumps({
                'operation': 'search',
                'data': {
                    'term': 'alpine'
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Images not searched')
        self.assertGreaterEqual(json.loads(response.data)['total'],  0,
                                'Images not searched')

    def test_history_image(self):
        response = self.app.post(
            self.path + '/image',
            headers=self.headers,
            data=json.dumps({
                'operation': 'pull',
                'data': {
                    'repository': 'alpine:latest'
                }
            })
        )
        self.assertEqual(response.status_code, 200, 'Image not pulled')

        response = self.app.post(
            self.path + '/image/single',
            headers=self.headers,
            data=json.dumps({
                'name': 'alpine',
                'operation': 'history',
                'data': {}
            })
        )
        self.assertEqual(response.status_code, 200, 'No history fetched')
        self.assertEqual(json.loads(response.data), {}, 'History available')
