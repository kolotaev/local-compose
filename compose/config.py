import yaml
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
        data = self._read_data()
        error = self.validate(data)
        return data

    def validate(self, data):
        try:
            jsonschema.validate(instance=data, schema=JSON_SCHEMA)
        except Exception as e:
            raise Exception('Configuration file %s is invalid.\nErrors found: %s' % (self._filename, e))

    def _read_data(self):
        data = None
        with open(self._filename) as file:
            try:
                data = yaml.safe_load(file)
            except Exception as e:
                print('Config yaml file structure is malformed.\nError: %s' % e)
        return data
