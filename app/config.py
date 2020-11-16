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

    @staticmethod
    def colors():
        return (
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
            "bright_black",
            "bright_red",
            "bright_green",
            "bright_yellow",
            "bright_blue",
            "bright_magenta",
            "bright_cyan",
            "bright_white",
        )
