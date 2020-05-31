import unittest

from src.classes.docker_engine import DockerEngine


class DeployImageTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DeployImageTests, self).__init__(*args, **kwargs)

    def test_get_client(self):
        client = DockerEngine().get_client()
        self.assertNotEqual(client, None, 'Engine does not exist')

    def test_pull_and_remove_image(self):
        response = DockerEngine().run_image_operation(
            operation='pull',
            data={
                'repository': 'alpine:latest'
            }
        )
        self.assertNotEqual(response, None, 'Pull image failed')

        response = DockerEngine().run_image_operation(
            operation='remove',
            data={
                'image': 'alpine',
                'force': True
            }
        )
        self.assertEqual(response, None, 'Remove image failed')

    def test_get_image(self):
        response = DockerEngine().run_image_operation(
            operation='pull',
            data={
                'repository': 'alpine:latest'
            }
        )
        self.assertNotEqual(response, None, 'Pull image failed')

        response = DockerEngine().run_image_operation(
            operation='get',
            data={
                'name': 'alpine'
            }
        )
        self.assertNotEqual(response, None, 'Pull get failed')
        self.assertNotEqual(response.short_id, None, 'Wrong ID')
        self.assertEqual(response.tags, ['alpine:latest'], 'Wrong tag')

    def test_prune_images(self):
        response = DockerEngine().run_image_operation(
            operation='prune',
            data={
                'filters': {
                    'dangling': True
                }
            }
        )
        self.assertNotEqual(response, None, 'Prune image failed')

    def test_search_image(self):
        response = DockerEngine().run_image_operation(
            operation='search',
            data={
                'term': 'alpine'
            }
        )
        self.assertNotEqual(response, None, 'Search images failed')
        self.assertIsInstance(response, list, 'Response is not a list')

    def test_history_image(self):
        image = DockerEngine().run_image_operation(
            operation='get',
            data={
                'name': 'alpine'
            }
        )
        self.assertNotEqual(image, False, 'Image not exists')

        response = DockerEngine().run_operation_in_object(
            object=image,
            operation='history',
            data={}
        )
        self.assertIsInstance(response, list, 'Wrong history')

    def test_reload_image(self):
        image = DockerEngine().run_image_operation(
            operation='pull',
            data={
                'repository': 'alpine:latest'
            }
        )
        self.assertNotEqual(image, False, 'Image not exists')

        response = DockerEngine().run_operation_in_object(
            object=image,
            operation='reload',
            data={}
        )
        self.assertNotEqual(response, False, 'Image not reloaded')
