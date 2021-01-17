from __future__ import print_function
import sys
from abc import ABCMeta

import colored

from .utils import now


# todo - move to separate module
class Message(object):
    '''
    Represents a basic messaging entity in the system.
    '''

    __metaclass__ = ABCMeta

    def __init__(self, data, name, time=None, color=None):
        self.data = data
        self.name = name
        self.color = color
        if time is None:
            self.time = now()
        else:
            self.time = time


class MessageOutput(Message):
    '''
    Message type for Service and system information logging and output.
    '''


class MessageStart(Message):
    '''
    Message type for Service starting.
    '''


class MessageStop(Message):
    '''
    Message type for Service stopping.
    '''


class MessageRestart(Message):
    '''
    Message type for Service restarting.
    '''


class MessageEmptyBus(Message):
    '''
    Message type that denotes empty message bus and thus finish of all components run.
    '''


class SimplePrintWriter(object):
    '''
    Basic writer that uses `print` function.
    Doesn't use colors.
    '''
    @staticmethod
    def write(message, color=None):
        'Write a message'
        print(message)


class ColoredPrintWriter(object):
    '''
    Writer that uses `colored` lib functionality.
    Can use 8-bit palette: 256 colors.
    '''
    @staticmethod
    def write(message, color=None):
        '''
        Write a message
        '''
        if color is None or not sys.stdout.isatty():
            print(message)
        else:
            print(colored.stylize(message, colored.fg(color)))

    @staticmethod
    def supported_colors():
        '''
        Get colors supported by the printer.
        '''
        return colored.colors.names


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
        if not isinstance(message, MessageOutput):
            raise RuntimeError('Printer can only process messages of type "%s"' % MessageOutput.__name__)

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
