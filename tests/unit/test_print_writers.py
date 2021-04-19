# -*- coding: utf-8 -*-

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import mock

from compose.printing import SimplePrintWriter, ColoredPrintWriter


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
def test_simple_print_writer_no_do_log(mock_stdout):
    w = SimplePrintWriter(do_log=False)
    w.write('hey i must not be printed')
    assert mock_stdout.getvalue() == ''


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
    assert mock_stdout.getvalue() == '\033[38;5;1mis there a color?\033[0m\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_colored_print_writer_color_no_tty(mock_stdout):
    mock_stdout.isatty = lambda: False
    w = ColoredPrintWriter()
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == 'is there a color?\n'


@mock.patch('sys.stdout', new_callable=StringIO, create=True)
def test_colored_print_writer_no_do_log(mock_stdout):
    w = ColoredPrintWriter(do_log=False)
    w.write('hey i must not be printed')
    assert mock_stdout.getvalue() == ''
