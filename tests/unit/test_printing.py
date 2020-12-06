# -*- coding: utf-8 -*-

from StringIO import StringIO

import mock

from compose.printing import SimplePrintWriter, ClickEchoWriter


@mock.patch('sys.stdout', new_callable=StringIO)
def test_simple_print_writer(mock_stdout):
    w = SimplePrintWriter()
    w.write(u'hello it is ü')
    assert mock_stdout.getvalue() == u'hello it is ü\n'
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == 'is there a color?\n'


@mock.patch('sys.stdout', new_callable=StringIO)
def test_simple_print_writer_color(mock_stdout):
    w = SimplePrintWriter()
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == 'is there a color?\n'


@mock.patch('sys.stdout', new_callable=StringIO)
def test_click_echo_writer(mock_stdout):
    w = ClickEchoWriter()
    w.write(u'hello it is ü')
    assert mock_stdout.getvalue() == u'hello it is ü\n'


@mock.patch('sys.stdout', new_callable=StringIO)
def test_click_echo_writer_color(mock_stdout):
    w = ClickEchoWriter()
    w.write('is there a color?', color='red')
    assert mock_stdout.getvalue() == '////is there a color?\n'
