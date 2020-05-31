from ansible import context
from ansible.cli import CLI
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager

from io import TextIOWrapper, BytesIO
import sys


from config.server_environment import ANSIBLE_PATH
from src.classes.ansible.host import Host
from src.classes.ansible.playbook import Playbook
from src.classes.mongo_engine import MongoEngine
from src.utils.dump_to_file import hosts_to_file


class AnsibleEngine:
    def __init__(self):
        self.path = ANSIBLE_PATH

    """
        Runs a playbook in the given hosts.
    """
    def run_playbook(self, hosts, playbook, passwords={}):
        if not hosts or not playbook:
            return False

        domain = MongoEngine().get_collection_name()

        # Check if hosts exists
        h = []
        if type(hosts) is list:
            for host in hosts:
                current = Host().find(criteria={'name': host})
                if current.data:
                    h.append({
                        'name': current.data['name'],
                        'ips': current.data['ips']
                    })
        else:
            return False

        if len(h) == 0:
            return False

        hosts_file = hosts_to_file(
            hosts=h,
            domain=domain,
            root=self.path,
            base_path='ansible',
            sub_path='hosts'
        )

        # Check if playbook exists
        pb = None
        current = Playbook().find(criteria={'name': playbook})
        if current.data:
            pb = current.data['playbook'][0]

        if not pb:
            return False

        # Ansible stuff
        loader = DataLoader()
        context.CLIARGS = ImmutableDict(
            tags={},
            listtags=False,
            listtasks=False,
            listhosts=False,
            syntax=False,
            connection='ssh',
            module_path=None,
            forks=10,
            private_key_file=None,
            ssh_common_args=None,
            ssh_extra_args=None,
            sftp_extra_args=None,
            scp_extra_args=None,
            force_handlers=None,
            become_method='sudo',
            become_user='root',
            verbosity=True,
            check=False,
            start_at_task=None
        )

        inventory = InventoryManager(
            loader=loader,
            sources=(hosts_file,)
        )

        variable_manager = VariableManager(
            loader=loader,
            inventory=inventory,
            version_info=CLI.version_info(gitinfo=False)
        )

        play = Play().load(
            pb,
            variable_manager=variable_manager,
            loader=loader
        )

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                passwords=passwords
            )

            sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

            tqm.run(play)

            sys.stdout.seek(0)
            result = sys.stdout.read()

            sys.stdout.close()
            sys.stdout = sys.__stdout__

        finally:
            if tqm is not None:
                tqm.cleanup()

        return result
