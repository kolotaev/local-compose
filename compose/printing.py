from __future__ import print_function

import click
import colored

from .utils import now


class Message(object):
    '''
    Represents a basic messaging entity in the system.
    '''
    def __init__(self, type, data, name, time=now(), color=None):
        self.type = type
        self.data = data
        self.name = name
        self.color = color
        self.time = time


class SimplePrintWriter(object):
    '''
    Basic writer that uses `print` function.
    Doesn't use colors.
    '''
    def write(self, message, color=None):
        'Write a message'
        print(message)


class ColoredPrintWriter(object):
    '''
    Writer that uses `colored` lib functionality.
    '''
    def write(self, message, color=None):
        '''
        Write a message
        '''
        if color is None:
            print(message)
        else:
            print(colored.stylize(message, colored.fg(color)))

    @staticmethod
    def available_colors():
        return colored.colors.names


class ClickEchoWriter(object):
    '''
    Writer that uses Click printing functionality.
    Uses ANSI colors if asked to do so.
    '''
    def __init__(self):
        self._click_module = click

    def write(self, message, color=None):
        'Write a message'
        self._click_module.echo(self._click_module.style(message, fg=color))


class Printer(object):
    '''
    Prints messages. For this it uses a specific writer for this purpose.
    In general, it's a smart facade for a Writer.
    '''
    def __init__(self, writer, time_format=None, use_prefix=True):
        self.writer = writer
        if time_format is None:
            self.time_format = '%H:%M:%S'
        else:
            self.time_format = time_format
        self.width = 0
        self.use_prefix = use_prefix

    def write(self, message):
        '''
        Writes message via underlying writer
        '''
        if message.type != 'output':
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
        '''
        Sets maximal width for info column based on langest service name
        '''
        self.width = max(self.width, len(service.name))
