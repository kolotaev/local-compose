import yaml
from six import with_metaclass

from .utils import Singleton

class Config(with_metaclass(Singleton, object)):
    def __init__(filename):
        self._filename = filename

    def parse(self):
        with open(self._filename) as file:
            try:
                data = yaml.parse(self._filename)
                return data
            except Exception as e:
                print('Config file is malformed. Error: %s' % e)
                return None
