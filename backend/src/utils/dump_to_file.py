import os
from datetime import datetime as dt


def create_path_if_not_exists(domain, root, base_path, sub_path):
    ansible_path = root + base_path + '/'
    hosts_path = ansible_path + sub_path + '/'
    domain_path = hosts_path + domain + '/'

    if not os.path.exists(ansible_path):
        os.mkdir(ansible_path)
    if not os.path.exists(hosts_path):
        os.mkdir(hosts_path)
    if not os.path.exists(domain_path):
        os.mkdir(domain_path)

    return domain_path


def hosts_to_file(hosts, domain, root, base_path, sub_path, filename=None):
    if not hosts or not domain or not base_path or not root or not sub_path:
        return False

    if not filename:
        filename = dt.isoformat(dt.utcnow())

    path = create_path_if_not_exists(
        domain=domain,
        root=root,
        sub_path=sub_path,
        base_path=base_path
    )

    file_path = path + filename
    if os.path.exists(file_path):
        os.remove(file_path)
    file = open(file_path, 'w+')

    if type(hosts) is list:
        for host in hosts:
            file.write('[' + host['name'] + ']')
            file.write('\n')
            for ip in host['ips']:
                file.write(ip)
                file.write('\n')

    file.close()

    return file_path


def yaml_to_file(data, domain, root, base_path, sub_path, filename=None):
    if not data or not domain or not base_path or not root or not sub_path:
        return False

    if not filename:
        filename = dt.isoformat(dt.utcnow())

    path = create_path_if_not_exists(
        domain=domain,
        root=root,
        sub_path=sub_path,
        base_path=base_path
    )
    file_path = path + filename + '.yaml'

    if os.path.exists(file_path):
        os.remove(file_path)
    file = open(file_path, 'w+')
    file.write('---\n')
    file.write(data)
    file.close()

    return file_path
