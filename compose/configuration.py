from __future__ import print_function
import sys
import os
import os.path
import difflib

import yaml
import jsonschema

from .schema import JSON_SCHEMA
from .service import Service
from .info import CONFIG_EXAMPLE
from .printing import ColoredPrintWriter


class Config(object):
    '''
    Main and only class that is responsible for configuration.
    '''
    def __init__(self, filename):
        self._filename = filename
        self._conf = None

    @staticmethod
    def example():
        '''
        Return configuration file example text in yaml format.
        '''
        return CONFIG_EXAMPLE

    @staticmethod
    def available_colors():
        '''
        List of colors allowed for usage in service output.
        '''
        return list(map(lambda x: x.lower(), ColoredPrintWriter.supported_colors()))

    def parse(self):
        '''
        Parses the config file.
        Validates it.
        Returns a configuration dict.
        '''
        try:
            contents = self.read()
            data = yaml.safe_load(contents)
            self._conf = data
            self.validate(data)
            return self
        except Exception as e:
            raise ConfigurationError('Configuration file "%s" is invalid.\nErrors found:\n%s' % (self._filename, e))

    def try_parse(self):
        '''
        Like parse but exits with error if errors are found.
        '''
        try:
            return self.parse()
        except ConfigurationError as e:
            print(e)
            sys.exit(1)

    def validate(self, data):
        '''
        Validates the config.
        '''
        if data is None:
            raise ConfigurationError('File is empty.')
        jsonschema.validate(instance=data, schema=JSON_SCHEMA)
        self._validate_services()

    def read(self):
        '''
        Read configuration from file.
        '''
        if not os.path.isfile(self._filename):
            raise ConfigurationError('File is not found.')
        with open(self._filename) as file:
            return file.read()

    @property
    def services(self):
        '''
        Build and get Service objects.
        '''
        services = []
        for name, srv_conf in self._conf.get('services', {}).items():
            # if srv.get('cwd'):
            #     cwd = os.path.join(os.getcwd(), srv.get('cwd'))
            # else:
            #     cwd = None
            params = {}
            if 'env' in srv_conf:
                params['env'] = srv_conf['env']
            if 'cwd' in srv_conf:
                params['cwd'] = srv_conf['cwd']
            if 'silent' in srv_conf:
                params['quiet'] = srv_conf['silent']
            if 'color' in srv_conf:
                params['color'] = srv_conf['color']
            if 'shell' in srv_conf:
                params['shell'] = srv_conf['shell']
            if 'readiness' in srv_conf:
                params['readiness'] = srv_conf['readiness']
            s = Service(name, srv_conf.get('run'), **params)
            services.append(s)
        return services

    @property
    def settings(self):
        '''
        Get settings.
        '''
        return self._conf.get('settings', {})

    @property
    def logging(self):
        '''
        Get logging settings.
        '''
        return self.settings.get('logging', {})

    @property
    def version(self):
        '''
        Get config file version.
        '''
        return self._conf.get('version')

    def _validate_services(self):
        '''
        Validate each service config properties
        '''
        allowed_colors = self.available_colors()
        for srv in self.services:
            if srv.color is None:
                continue
            if srv.color not in allowed_colors:
                suggested_colors = difflib.get_close_matches(srv.color, allowed_colors, n=1)
                msg = "Color '%s' for service '%s' is not allowed." % (srv.color, srv.name)
                if suggested_colors:
                    msg += '\nMaybe you meant: %s' % suggested_colors[0]
                raise ConfigurationError(msg)


class ConfigurationError(ValueError):
    '''
    Configuration error.
    '''
