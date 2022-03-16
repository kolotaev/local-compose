# -*- coding: utf-8 -*-

import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import mock
import pytest
import colored

from compose.printing import SimplePrintWriter, ColoredPrintWriter, WritersFactory


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_simple_print_writer(mock_stdout):
    w = SimplePrintWriter()
    w.write(u'hello it is ü')
    assert mock_stdout.getvalue() == u'hello it is ü\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_simple_print_writer_color(mock_stdout):
    w = SimplePrintWriter()
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == 'is there a color?\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_colored_print_writer(mock_stdout):
    w = ColoredPrintWriter()
    w.write('hello it is û')
    assert mock_stdout.getvalue() == 'hello it is û\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_colored_print_writer_color(mock_stdout):
    colored.set_tty_aware(False)
    w = ColoredPrintWriter()
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == '\033[38;5;1mis there a color?\033[0m\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_colored_print_writer_color_no_tty(mock_stdout):
    colored.set_tty_aware(True)
    w = ColoredPrintWriter()
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == 'is there a color?\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
@mock.patch.dict(os.environ, {'FORCE_COLOR': '1'}, clear=True)
def test_colored_print_writer_respects_force_color_env(mock_stdout):
    w = ColoredPrintWriter()
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == '\033[38;5;1mis there a color?\033[0m\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
@mock.patch.dict(os.environ, {'NO_COLOR': '1'}, clear=True)
def test_colored_print_writer_respects_no_color_env(mock_stdout):
    colored.set_tty_aware(False)
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


@pytest.mark.parametrize('is_enabled, expect_loggers', [
    (True, 2),
    (False, 1),
])
def test_writers_factory_logging_to_file_with_enabled_flag(is_enabled, expect_loggers):
    config = mock.Mock()
    config.logging = {
        'toFile': {
            'enabled': is_enabled,
        },
    }
    config.services = {}
    ws = WritersFactory(config, '/path/to/store', True).create()
    assert len(ws) == expect_loggers
