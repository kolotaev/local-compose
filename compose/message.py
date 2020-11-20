from collections import namedtuple
import sys


Message = namedtuple('Message', 'type data time name color')


class ClickEchoWriter():
    def write(self, message, color=None):
        pass


class Printer(object):
    def __init__(self, writer, time_format='%H:%M:%S', width=0, prefix=True):
        self.writer = writer
        self.time_format = time_format
        self.width = width
        self.color = color
        self.prefix = prefix

    def write(self, message):
        if message.type != 'line':
            raise RuntimeError('Printer can only process messages of type "line"')

        name = message.name if message.name is not None else ''
        name = name.ljust(self.width)
        if name:
            name += " "

        # Replace the unrecognisable bytes with Unicode replacement character (U+FFFD).
        if isinstance(message.data, bytes):
            string = message.data.decode('utf-8', 'replace')
        else:
            string = message.data

        for line in string.splitlines():
            prefix = ''
            if self.prefix:
                time_formatted = message.time.strftime(self.time_format)
                prefix = '{time} {name}| '.format(time=time_formatted, name=name)
            self.writer.write(line, color)
