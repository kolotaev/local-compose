from __future__ import print_function
import sys
import os
import os.path

import yaml
import jsonschema

from .schema import JSON_SCHEMA
from .service import Service


class Config(object):
    def __init__(self, filename):
        self._filename = filename
        self._conf = None

    @staticmethod
    def example():
        return ''

    def parse(self):
        '''
        Parses the config file.
        Validates it.
        Returns a configuration dict.
        '''
        try:
            contents = self.read()
            data = yaml.safe_load(contents)
            self.validate(data)
            self._conf = data
            return self
        except Exception as e:
            raise Exception('Configuration file "%s" is invalid.\nErrors found:\n%s' % (self._filename, e))

    def try_parse(self):
        '''
        Like parse but exits with error if errors are found.
        '''
        try:
            return self.parse()
        except Exception as e:
            print(e)
            sys.exit(1)

    def validate(self, data):
        '''
        Validates the config.
        '''
        if data is None:
            raise ValueError('File is empty.')
        jsonschema.validate(instance=data, schema=JSON_SCHEMA)

    def read(self):
        if not os.path.isfile(self._filename):
            raise Exception('File is not found.')
        with open(self._filename) as file:
            return file.read()

    @property
    def services(self):
        '''
        Build and get Service objects.
        '''
        services = []
        for name, srv in self._conf['services'].items():
            if srv.get('cwd'):
                cwd = os.path.join(os.getcwd(), srv.get('cwd'))
            else:
                cwd = None
            env = {}
            s = Service(name, srv.get('run'),
                        quiet=srv.get('quite'), color=srv.get('color'),
                        env=env, cwd=cwd)
            services.append(s)
        return services

    @property
    def settings(self):
        '''
        Get global settings.
        '''
        return self._conf['global']

    @property
    def version(self):
        '''
        Get config file version.
        '''
        return self._conf['version']
