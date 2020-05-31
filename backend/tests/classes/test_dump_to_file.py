import unittest
import os
import shutil

from src.classes.ansible.host import Host
from src.classes.ansible.playbook import Playbook
from src.classes.customer import Customer
from src.classes.mongo_engine import MongoEngine

from src.utils.dump_to_file import hosts_to_file, yaml_to_file,\
    create_path_if_not_exists

from config.server_environment import TESTING_DATABASE


class DumpTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DumpTests, self).__init__(*args, **kwargs)

        # Drop previous database
        Customer().set_customer(TESTING_DATABASE)
        MongoEngine().drop_collection(TESTING_DATABASE, 'hosts')
        MongoEngine().drop_collection(TESTING_DATABASE, 'playbooks')

        self.root = './'
        self.base_path = 'files-generated'
        self.domain = 'domain.com'
        self.sub_path_hosts = 'hosts'
        self.sub_path_playbooks = 'playbooks'

    def test_create_path(self):
        path = create_path_if_not_exists(
            root=self.root,
            domain=self.domain,
            base_path=self.base_path,
            sub_path='type-of-file'
        )

        self.assertEqual(os.path.exists(path), True, 'Path non existing')
        shutil.rmtree('./files-generated', ignore_errors=False, onerror=None)

    def test_dump_hosts_to_file_without_name(self):
        Host().insert({
            'name': 'host1',
            'ips': ['192.168.1.5', '192.168.2.5']
        })

        host = Host().find()
        self.assertNotEqual(host, None, 'Host obj not found')

        path = hosts_to_file(
            hosts=[host.data],
            domain=self.domain,
            root=self.root,
            base_path=self.base_path,
            sub_path=self.sub_path_hosts
        )

        self.assertEqual(os.path.exists(path), True, 'File does not exists')
        file = open(path, 'r')
        content = '[host1]\n192.168.1.5\n192.168.2.5\n'
        self.assertEqual(file.read(), content, 'File content is not correct')
        shutil.rmtree('./files-generated', ignore_errors=False, onerror=None)

    def test_dump_hosts_to_file_with_name(self):
        Host().insert({
            'name': 'host1',
            'ips': ['192.168.1.5', '192.168.2.5']
        })

        host = Host().find()
        self.assertNotEqual(host, None, 'Host obj not found')

        path = hosts_to_file(
            hosts=[host.data],
            domain=self.domain,
            root=self.root,
            base_path=self.base_path,
            sub_path=self.sub_path_hosts,
            filename='cool-name'
        )

        self.assertEqual(os.path.exists(path), True, 'File does not exists')
        file = open(path, 'r')
        content = '[host1]\n192.168.1.5\n192.168.2.5\n'
        self.assertEqual(file.read(), content, 'File content is not correct')
        shutil.rmtree('./files-generated', ignore_errors=False, onerror=None)

    def test_dump_yaml_to_file_without_name(self):
        Playbook().insert({
            'name': 'cool-playbook',
            'playbook': {
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
        })

        playbook = Playbook().find()
        self.assertNotEqual(playbook, None, 'Playbook obj not found')
        yaml_playbook = playbook.parse_yaml()

        path = yaml_to_file(
            data=yaml_playbook,
            domain=self.domain,
            root=self.root,
            base_path=self.base_path,
            sub_path=self.sub_path_playbooks
        )

        self.assertEqual(os.path.exists(path), True, 'File does not exists')
        file = open(path, 'r')

        content = '---\n- hosts: test\n  remote_user: test1\n  tasks:' \
                  '\n  - debug:\n      msg: Debug msg\n    name: test debug\n'

        self.assertEqual(file.read(), content, 'File content is not correct')
        shutil.rmtree('./files-generated', ignore_errors=False, onerror=None)

    def test_dump_yaml_to_file_without_name(self):
        Playbook().insert({
            'name': 'cool-playbook',
            'playbook': {
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
        })

        playbook = Playbook().find()
        self.assertNotEqual(playbook, None, 'Playbook obj not found')
        yaml_playbook = playbook.parse_yaml()

        path = yaml_to_file(
            data=yaml_playbook,
            domain=self.domain,
            root=self.root,
            base_path=self.base_path,
            sub_path=self.sub_path_playbooks,
            filename='cool-name'
        )

        self.assertEqual(os.path.exists(path), True, 'File does not exists')
        file = open(path, 'r')

        content = '---\n- hosts: test\n  remote_user: test1\n  tasks:' \
                  '\n  - debug:\n      msg: Debug msg\n    name: test debug\n'

        self.assertEqual(file.read(), content, 'File content is not correct')
        shutil.rmtree('./files-generated', ignore_errors=False, onerror=None)
