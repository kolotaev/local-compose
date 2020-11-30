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
        pass

    @staticmethod
    def colors():
        return (
            'black',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
            'bright_black',
            'bright_red',
            'bright_green',
            'bright_yellow',
            'bright_blue',
            'bright_magenta',
            'bright_cyan',
            'bright_white',
        )

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

    def _read_data(self):
        data = None
        with open(self._filename) as file:
            try:
                data = yaml.safe_load(file)
            except Exception as e:
                raise Exception('Config yaml file structure is malformed.\nError found:\n%s' % e)
        return data
