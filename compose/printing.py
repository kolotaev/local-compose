from __future__ import print_function
import sys

import colored

from .messaging import Line, SYSTEM_LABEL


# import logging
# import time
# from logging.handlers import TimedRotatingFileHandler
# #----------------------------------------------------------------------
# def create_timed_rotating_log(path):
#     """"""
#     logger = logging.getLogger("Rotating Log")
#     logger.setLevel(logging.INFO)

#     handler = TimedRotatingFileHandler(path,
#                                        when="m",
#                                        interval=1,
#                                        backupCount=5)
#     logger.addHandler(handler)

#     for i in range(6):
#         logger.info("This is a test!")
#         time.sleep(75)
# #----------------------------------------------------------------------
# if __name__ == "__main__":
#     log_file = "timed_test.log"
#     create_timed_rotating_log(log_file)


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
        # todo - color only
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
                w.write(prefix + line, color=message.color)

    def adjust_width(self, service):
        '''
        Sets maximal width for info column based on langest service name
        '''
        self.width = max(self.width, len(service.name))
