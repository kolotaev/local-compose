from __future__ import print_function
import sys
import datetime


def now():
    return


class Message(object):
    def __init__(self, type, data, name, time=None, color=None):
        self.type = type
        self.data = data
        self.name = name
        self.color = color
        if time is None:
            time = self.now()
        self.time = time

    @staticmethod
    def now():
        return datetime.datetime.now()


class PrintWriter(object):
    def write(self, message, color=None):
        print(message)


class ClickEchoWriter(object):
    def __init__(self):
        import click
        self._click_module = click

    def write(self, message, color=None):
        self._click_module.echo(self._click_module.style(message, fg=color))


class Printer(object):
    def __init__(self, writer, time_format='%H:%M:%S', width=0, prefix=True):
        self.writer = writer
        self.time_format = time_format
        self.width = width
        self.prefix = prefix

    def write(self, message):
        if message.type != 'line':
            raise RuntimeError('Printer can only process messages of type "line"')

        name = message.name if message.name is not None else ''
        name = name.ljust(self.width)
        if name:
            name += ' '

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
            self.writer.write(prefix + line, color=message.color)
