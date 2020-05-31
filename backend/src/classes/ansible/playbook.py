import yaml

from src.classes.item import Item


class Playbook(Item):
    table_name = 'playbooks'
    table_schema = {
        'name': 1,
        'playbook': 1,
        'deleted': 1
    }

    def __init__(self):
        super(Playbook, self).__init__()

    """
        Inserts a new playbook.
    """
    def insert(self, data=None):
        if data is not None:
            current = super(Playbook, self) \
                .find(criteria={'name': data['name']})

            data['playbook'] = [data['playbook']]

            if not current.data:
                return super(Playbook, self).insert(data)

        return False

    """
        Parses the current playbook to YAML format.
    """
    def parse_yaml(self):
        if self.data:
            return yaml.dump(self.data['playbook'])
