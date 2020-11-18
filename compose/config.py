import sys

import yaml
import six
import jsonschema
# from six import with_metaclass

# from .utils import Singleton
from .schema import JSON_SCHEMA


class Config(object):
    def __init__(self, filename):
        self._filename = filename

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
        """
        Parses the config file.
        Validates it.
        Returns a configuration dict.
        """
        data = self._read_data()
        error = self.validate(data)
        return data

    def try_parse(self):
        """
        Like parse but exits with error if errors are found.
        """
        data = None
        try:
            return self.parse()
        except Exception as e:
            six.print_(e)
            sys.exit(1)

    def validate(self, data):
        """
        Validates the config.
        """
        try:
            jsonschema.validate(instance=data, schema=JSON_SCHEMA)
        except Exception as e:
            raise Exception('Configuration file "%s" is invalid.\nErrors found:\n%s' % (self._filename, e))

    def _read_data(self):
        data = None
        with open(self._filename) as file:
            try:
                data = yaml.safe_load(file)
            except Exception as e:
                raise Exception('Config yaml file structure is malformed.\nError found: %s' % e)
        return data
