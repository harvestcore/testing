import unittest

from src.classes.docker_engine import DockerEngine
from src.classes.ansible.ansible_engine import AnsibleEngine
from src.classes.ansible.playbook import Playbook
from src.classes.ansible.host import Host
from src.classes.customer import Customer
from src.classes.mongo_engine import MongoEngine

from config.server_environment import TESTING_DATABASE


class AnsibleEngineTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AnsibleEngineTests, self).__init__(*args, **kwargs)

        # Drop previous database
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'hosts')
        MongoEngine().drop_collection(TESTING_DATABASE, 'playbooks')

    def test_run_playbook(self):
        self.playbook = 'test-alpine-ssh'
        self.hosts = ['alpine']
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
            'ips': [ips]
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

        response = AnsibleEngine().run_playbook(
            hosts=self.hosts,
            playbook=self.playbook,
            passwords={
                'conn_pass': 'root',
                'become_pass': 'root'
            }
        )

        self.assertNotEqual(response, False, 'Playbook did not run')
        self.assertNotEqual(response.find('PLAY [alpine]'), -1)

        c = DockerEngine().get_container_by_id(self.container_id)
        DockerEngine().run_operation_in_object(
            object=c,
            operation='stop',
            data={}
        )
