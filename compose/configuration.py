from __future__ import print_function
import sys

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
        data = self._read_data()
        self.validate(data)
        self._conf = data
        return self

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
        try:
            if data is None:
                raise ValueError('Empty file.')
            jsonschema.validate(instance=data, schema=JSON_SCHEMA)
        except Exception as e:
            raise Exception('Configuration file "%s" is invalid.\nErrors found:\n%s' % (self._filename, e))

    @property
    def services(self):
        '''
        Build and get Service objects.
        '''
        services = []
        import os
        import os.path
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

    def _read_data(self):
        with open(self._filename) as file:
            try:
                return yaml.safe_load(file)
            except Exception as e:
                raise Exception('Configuration file "%s" is invalid.\nError found:\n%s' % (self._filename, e))
        return None
