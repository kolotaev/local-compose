import os
import signal
import subprocess

from .printing import Message
from .utils import now


class Executor(object):
    pass


class Pool(object):
    def __init__(self):
        self._elements = {}

    def add(self, name, process):
        self._elements[name] = {
            'proc': process
        }

    def all(self):
        return self._elements.items()

    def get(self, name):
        return self._elements.get(name)

    def set_rc(self, name, returncode):
        self._elements[name]['returncode'] = returncode

    def set_pid(self, name, pid):
        self._elements[name]['pid'] = pid

    def all_started(self):
        return all(p.get('pid') is not None for _, p in self._elements.items())

    def all_stopped(self):
        return all(p.get('returncode') is not None for _, p in self._elements.items())

    def any_stopped(self):
        return any(p.get('returncode') is not None for _, p in self._elements.items())
