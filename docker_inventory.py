#!/usr/bin/env python
from argparse import ArgumentParser
from copy import deepcopy
from json import dumps

from docker import DockerClient


class DockerInventory(object):

    _data_structure = {'all': {'hosts': []}, '_meta': {'hostvars': {}}}

    def __init__(self, option):
        self.docker = DockerClient()

        if option.list:
            data = self.containers()
        elif option.host:
            data = self.containers_by_host(option.host)
        else:
            data = self._data_structure
        print(dumps(data))

    def get_containers(self):
        return self.docker.containers.list(all=True)

    def containers(self):
        resdata = deepcopy(self._data_structure)
        for container in self.get_containers():
            resdata['all']['hosts'].append(container.name)
            resdata['_meta']['hostvars'][container.name] = \
                {'ansible_connection': 'docker'}

        return resdata

    def containers_by_host(self, host=None):
        resdata = deepcopy(self._data_structure)
        for container in self.get_containers():
            if str(container.name) == host:
                resdata['all']['hosts'].append(container.name)
                resdata['_meta']['hostvars'][container.name] = \
                    {'ansible_connection': 'docker'}
                break

        return resdata


if __name__ == "__main__":
    dynamic_parser = ArgumentParser()
    dynamic_parser.add_argument('--list', action='store_true')
    dynamic_parser.add_argument('--host')

    DockerInventory(dynamic_parser.parse_args())
