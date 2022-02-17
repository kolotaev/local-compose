# -*- coding: utf-8 -*-

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import mock

from compose.printing import SimplePrintWriter, ColoredPrintWriter, WritersFactory
from compose.configuration import Config


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_simple_print_writer(mock_stdout):
    mock_stdout.isatty = lambda: True
    w = SimplePrintWriter()
    w.write(u'hello it is ü')
    assert mock_stdout.getvalue() == u'hello it is ü\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_simple_print_writer_color(mock_stdout):
    mock_stdout.isatty = lambda: True
    w = SimplePrintWriter()
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == 'is there a color?\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_colored_print_writer(mock_stdout):
    mock_stdout.isatty = lambda: True
    w = ColoredPrintWriter()
    w.write('hello it is û')
    assert mock_stdout.getvalue() == 'hello it is û\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_colored_print_writer_color(mock_stdout):
    mock_stdout.isatty = lambda: True
    w = ColoredPrintWriter()
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == '\x1b[38;5;1mis there a color?\x1b[0m\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_colored_print_writer_color_no_tty(mock_stdout):
    mock_stdout.isatty = lambda: False
    w = ColoredPrintWriter()
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == 'is there a color?\n'


def test_writers_factory_no_file_out():
    config = mock.Mock()
    config.logging = {}
    ws = WritersFactory(config, '/path/to/store', True).create()
    assert len(ws) == 1
    assert isinstance(ws[0], ColoredPrintWriter)
    ws = WritersFactory(config, '', False).create()
    assert len(ws) == 1
    assert isinstance(ws[0], SimplePrintWriter)


def test_writers_factory_file_out():
    config = mock.Mock()
    config.logging = {
        'toFile': {
            'maxSize': 5000,
        },
    }
    config.services = {}
    ws = WritersFactory(config, '/path/to/store', True).create()
    assert len(ws) == 2
