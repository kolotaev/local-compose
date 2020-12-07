from __future__ import print_function
import sys

from .utils import now


class Message(object):
    def __init__(self, type, data, name, time=now(), color=None):
        self.type = type
        self.data = data
        self.name = name
        self.color = color
        self.time = time


class SimplePrintWriter(object):
    def write(self, message, color=None):
        # sys.stdout.write
        print(message)


class ClickEchoWriter(object):
    def __init__(self):
        import click
        self._click_module = click

    def write(self, message, color=None):
        self._click_module.echo(self._click_module.style(message, fg=color))


class Printer(object):
    def __init__(self, writer, time_format='%H:%M:%S', use_prefix=True):
        self.writer = writer
        if time_format is None:
            self.time_format = '%H:%M:%S'
        else:
            self.time_format = time_format
        self.width = 0
        self.use_prefix = use_prefix

    def write(self, message):
        if message.type != 'line':
            raise RuntimeError('Printer can only process messages of type "line"')

        if message.name is not None:
            name = message.name
        else:
            name = ''
        name = name.ljust(self.width)
        if name:
            name += ' '

        # Replace the unrecognizable bytes with Unicode replacement character (U+FFFD).
        if isinstance(message.data, bytes):
            string_data = message.data.decode('utf-8', 'replace')
        else:
            string_data = message.data

        lines = string_data.splitlines()
        if not lines:
            lines = ['']

        for line in lines:
            prefix = ''
            if self.use_prefix:
                time_formatted = message.time.strftime(self.time_format)
                prefix = '{time} {name}| '.format(time=time_formatted, name=name)
            self.writer.write(prefix + line, color=message.color)

    def adjust_width(self, service):
        self.width = max(self.width, len(service.name))
