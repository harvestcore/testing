import ipaddress
import re

from src.classes.item import Item


mac_regex = "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$"


class Machine(Item):
    table_name = 'machines'
    table_schema = {
        'name': 1,
        'description': 1,
        'type': 1,
        'ipv4': 1,
        'ipv6': 1,
        'mac': 1,
        'broadcast': 1,
        'gateway': 1,
        'netmask': 1,
        'network': 1,
        'deleted': 1
    }

    def __init__(self):
        super(Machine, self).__init__()

    """
        Inserts a new machine.
    """
    def insert(self, data=None):
        if data is not None:
            current = super(Machine, self) \
                .find(criteria={'name': data['name']})

            if not current.data:
                if self.validate_data(data):
                    return super(Machine, self).insert(data)

        return False

    """
        Updates a machine.
    """
    def update(self, criteria, data):
        if data is not None:
            if self.validate_data(data):
                return super(Machine, self).update(criteria, data)

        return False

    """
        Validates all the available (and optional) parameters that a machine
        can have.
    """
    @staticmethod
    def validate_data(data):
        if 'type' in data and data['type'] not in ['local', 'remote']:
            return False
        if 'ipv4' in data:
            try:
                ipaddress.IPv4Address(data['ipv4'])
            except ipaddress.AddressValueError:
                return False
        if 'ipv6' in data:
            try:
                ipaddress.IPv6Address(data['ipv6'])
            except ipaddress.AddressValueError:
                return False
        if 'mac' in data:
            if not re.match(mac_regex, data['mac'].lower()):
                return False
        if 'broadcast' in data:
            try:
                ipaddress.IPv4Address(data['broadcast'])
            except ipaddress.AddressValueError:
                return False
        if 'gateway' in data:
            try:
                ipaddress.IPv4Address(data['gateway'])
            except ipaddress.AddressValueError:
                return False
        if 'netmask' in data:
            try:
                ipaddress.IPv4Address(data['netmask'])
            except ipaddress.AddressValueError:
                return False
        if 'network' in data:
            try:
                ipaddress.IPv4Address(data['network'])
            except ipaddress.AddressValueError:
                return False

        return True
