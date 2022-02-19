from __future__ import print_function
import os
import logging
import logging.handlers

import colored

from .info import NAME
from .messaging import Line, SYSTEM_LABEL


class WritersFactory(object):
    '''
    Constructs a set of writers based on the global logging config.
    '''
    def __init__(self, config, store_temp_dir, use_color):
        self.conf = config
        self.use_color = use_color
        self.store_temp_dir = store_temp_dir

    def create(self):
        '''
        Create writers
        '''
        writers = []
        if self.use_color:
            stdout_writer = ColoredPrintWriter()
        else:
            stdout_writer = SimplePrintWriter()
        if self.conf.logging.get('toStdout', True):
            writers.append(stdout_writer)
        to_file_config = self.conf.logging.get('toFile', {})
        if to_file_config:
            fw = RotatingFileLogWriter(
                self.store_temp_dir,
                self.conf.services,
                to_file_config.get('maxSize', 0),
                to_file_config.get('backupCount', 0),
            )
            writers.append(fw)
        return writers


class RotatingFileLogWriter(object):
    '''
    Writer that writes data in the log files of a specified size, that are rotating on size exceed.
    '''
    def __init__(self, store_temp_dir, services, max_bytes, backup_count):
        self._loggers = {}
        for s in services:
            if s.log_to_file:
                file_path = s.log_to_file
            else:
                file_path = os.path.join(store_temp_dir, '%s.log' % s)
            handler = logging.handlers.RotatingFileHandler(file_path, maxBytes=max_bytes, backupCount=backup_count)
            logger = logging.getLogger('%s-%s' % (NAME, s.name))
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)
            self._loggers[s] = logger

    def write(self, message, color=None, service=None):
        '''
        Write a message
        '''
        if service in self._loggers:
            self._loggers[service].info(message)


class SimplePrintWriter(object):
    '''
    Basic writer that uses `print` function.
    Doesn't use colors.
    '''
    def write(self, message, color=None, service=None):
        '''
        Write a message
        '''
        print(message)


class ColoredPrintWriter(SimplePrintWriter):
    '''
    Writer that uses `colored` lib functionality.
    Can use 8-bit palette: 256 colors.
    '''
    def write(self, message, color=None, service=None):
        '''
        Write a message
        '''
        if color is None:
            msg = message
        else:
            msg = colored.stylize(message, colored.fg(color))
        super(ColoredPrintWriter, self).write(message=msg, color=color, service=service)

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
    def __init__(self, writers, time_format=None, use_prefix=True):
        self.writers = writers
        if time_format is None:
            self.time_format = '%H:%M:%S'
        else:
            self.time_format = time_format
        # The only known 'service' name that we know for sure at the begining
        self.width = len(SYSTEM_LABEL)
        self.use_prefix = use_prefix

    def write(self, message):
        '''
        Writes message via underlying writer
        '''
        if not isinstance(message, Line):
            raise RuntimeError('Printer can only process messages of type "%s"' % Line.__name__)

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
            for w in self.writers:
                w.write(prefix + line, color=message.color, service=name)

    def adjust_width(self, service):
        '''
        Sets maximal width for info column based on langest service name
        '''
        self.width = max(self.width, len(service.name))
