import yaml
import jsonschema
import jsonschema.exceptions
from six import with_metaclass

from .utils import Singleton
from .schema import JSON_SCHEMA


class Config(with_metaclass(Singleton, object)):
    def __init__(filename):
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
        except jsonschema.exceptions.ValidationError as e:
            raise e

    def _read_data(self):
        with open(self._filename) as file:
            try:
                data = yaml.parse(self._filename)
                return data
            except Exception as e:
                print('Config file structure is malformed. Error: %s' % e)
                return None
