import unittest

from src.classes.docker_engine import DockerEngine


class DeployContainerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DeployContainerTests, self).__init__(*args, **kwargs)

    def test_get_client(self):
        client = DockerEngine().get_client()
        self.assertNotEqual(client, None, 'Engine does not exist')

    # Container tests
    def test_run_hello_world_container(self):
        response = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'hello-world'
            }
        )
        self.assertNotEqual(response.decode().find('Hello from Docker!'), -1,
                            'Hello world run failed')

    def test_get_running_container(self):
        response = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'mongo:4.2.3',
                'detach': True
            }
        )
        self.assertNotEqual(response, None, 'Background container run failed')
        self.assertEqual(response.status, 'created', 'Container not created')

        response_get = DockerEngine().run_container_operation(
            operation='get',
            data={
                'container_id': response.short_id
            }
        )

        self.assertEqual(response_get.short_id, response.short_id,
                         'Image not found')

        container = DockerEngine().get_container_by_id(response.short_id)
        self.assertNotEqual(container, None, 'Container does not exist')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='stop',
            data={}
        )

        self.assertEqual(response, None, 'Container not stopped')

    def test_list_running_containers(self):
        response = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'mongo:4.2.3',
                'detach': True
            }
        )
        self.assertNotEqual(response, None, 'Background container1 run failed')
        self.assertEqual(response.status, 'created', 'Container1 not created')

        response2 = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'mongo:4.2.3',
                'detach': True
            }
        )
        self.assertNotEqual(response2, None,
                            'Background container2 run failed')
        self.assertEqual(response2.status, 'created', 'Container2 not created')

        response_list = DockerEngine().run_container_operation(
            operation='list',
            data={
                'all': False
            }
        )

        self.assertGreaterEqual(len(response_list), 2,
                                'Not all containers listed')

        response_list = DockerEngine().run_container_operation(
            operation='list',
            data={
                'all': False,
                'filters': {
                    'id': response.short_id
                }
            }
        )

        self.assertEqual(len(response_list), 1,
                         'Wrong number of container listed')
        self.assertEqual(response_list[0].short_id, response.short_id,
                         'Wrong container listed')

        container = DockerEngine().get_container_by_id(response.short_id)
        self.assertNotEqual(container, None, 'Container1 does not exist')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='stop',
            data={}
        )

        self.assertEqual(response, None, 'Container not stopped')

        container = DockerEngine().get_container_by_id(response2.short_id)
        self.assertNotEqual(container, None, 'Container2 does not exist')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='stop',
            data={}
        )

        self.assertEqual(response, None, 'Container not stopped')

    def test_run_and_stop_background_container(self):
        response = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'mongo:4.2.3',
                'detach': True
            }
        )
        self.assertNotEqual(response, None, 'Background image run failed')
        self.assertEqual(response.status, 'created', 'Container not created')

        container = DockerEngine().get_container_by_id(response.short_id)
        self.assertNotEqual(container, None, 'Container does not exist')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='stop',
            data={}
        )

        self.assertEqual(response, None, 'Container not stopped')

    def test_prune_containers(self):
        response = DockerEngine().run_container_operation(
            operation='prune',
            data={}
        )
        self.assertNotEqual(response, False, 'Prune all failed')

    def test_kill_container(self):
        response = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'mongo:4.2.3',
                'detach': True
            }
        )
        self.assertNotEqual(response, None, 'Background image run failed')
        self.assertEqual(response.status, 'created', 'Container not created')

        container = DockerEngine().get_container_by_id(response.short_id)
        self.assertNotEqual(container, None, 'Container does not exist')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='kill',
            data={}
        )

        self.assertEqual(response, None, 'Container not killed')

    def test_logs_container(self):
        response = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'mongo:4.2.3',
                'detach': True
            }
        )
        self.assertNotEqual(response, None, 'Background image run failed')
        self.assertEqual(response.status, 'created', 'Container not created')

        container = DockerEngine().get_container_by_id(response.short_id)
        self.assertNotEqual(container, None, 'Container does not exist')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='logs',
            data={}
        )

        self.assertIsInstance(response.decode(), str, 'Wrong container logs')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='stop',
            data={}
        )

        self.assertEqual(response, None, 'Container not stopped')

    def test_pause_unpause_container(self):
        response = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'mongo:4.2.3',
                'detach': True
            }
        )
        self.assertNotEqual(response, None, 'Background image run failed')
        self.assertEqual(response.status, 'created', 'Container not created')

        container = DockerEngine().get_container_by_id(response.short_id)
        self.assertNotEqual(container, None, 'Container does not exist')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='pause',
            data={}
        )

        self.assertEqual(response, None, 'Container not paused')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='unpause',
            data={}
        )

        self.assertEqual(response, None, 'Container not unpaused')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='stop',
            data={}
        )

        self.assertEqual(response, None, 'Container not stopped')

    def test_reload_container(self):
        response = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'mongo:4.2.3',
                'detach': True
            }
        )
        self.assertNotEqual(response, None, 'Background image run failed')
        self.assertEqual(response.status, 'created', 'Container not created')

        container = DockerEngine().get_container_by_id(response.short_id)
        self.assertNotEqual(container, None, 'Container does not exist')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='reload',
            data={}
        )

        self.assertEqual(response, None, 'Container not reloaded')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='stop',
            data={}
        )

        self.assertEqual(response, None, 'Container not stopped')

    def test_rename_container(self):
        response_run = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'mongo:4.2.3',
                'detach': True
            }
        )
        self.assertNotEqual(response_run, None, 'Background image run failed')
        self.assertEqual(response_run.status, 'created',
                         'Container not created')

        container = DockerEngine().get_container_by_id(response_run.short_id)
        self.assertNotEqual(container, None, 'Container does not exist')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='rename',
            data={
                'name': 'testing-name'
            }
        )

        self.assertEqual(response, None, 'Container not reloaded')

        container = DockerEngine().get_container_by_id(response_run.short_id)
        self.assertEqual(container.name, 'testing-name', 'Wrong name')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='stop',
            data={}
        )

        self.assertEqual(response, None, 'Container not stopped')

    def test_restart_container(self):
        response = DockerEngine().run_container_operation(
            operation='run',
            data={
                'image': 'mongo:4.2.3',
                'detach': True
            }
        )
        self.assertNotEqual(response, None, 'Background image run failed')
        self.assertEqual(response.status, 'created', 'Container not created')

        container = DockerEngine().get_container_by_id(response.short_id)
        self.assertNotEqual(container, None, 'Container does not exist')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='restart',
            data={}
        )

        self.assertEqual(response, None, 'Container not restarted')

        response = DockerEngine().run_operation_in_object(
            object=container,
            operation='stop',
            data={}
        )

        self.assertEqual(response, None, 'Container not stopped')
