from datetime import datetime
import time
import os

import pytest

from compose.printing import Printer, Message
from compose.service import Service


@pytest.fixture
def timezone_fixture():
    original_tz = os.environ.get('TZ')
    os.environ['TZ'] = 'Europe/London'
    time.tzset()
    yield
    if original_tz:
        os.environ['TZ'] = original_tz
    else:
        del os.environ['TZ']
    time.tzset()


class StoreWriter(object):
    def __init__(self):
        self.data = ''

    def write(self, msg, color=None):
        self.data = msg


def test_printer_does_not_allow_other_mesage_types():
    p = Printer(StoreWriter())
    with pytest.raises(RuntimeError) as execinfo:
        p.write(Message(type='close', data='bye...', name='web1'))
    assert 'Printer can only process messages of type "line"' == str(execinfo.value)


def test_adjust_width():
    p = Printer(StoreWriter())
    s1 = Service(name='web1', cmd='cat')
    s2 = Service(name='web_1234567890', cmd='cat')
    s3 = Service(name='web_2', cmd='cat')
    assert 0 == p.width
    p.adjust_width(s1)
    assert 4 == p.width
    p.adjust_width(s1)
    assert 4 == p.width
    p.adjust_width(s2)
    assert 14 == p.width
    p.adjust_width(s3)
    assert 14 == p.width


@pytest.mark.parametrize('message, time_format, use_prefix, expect', [
    (
        Message(type='line', data='', name=''),
        '',
        True,
        '        | '
    ),
    (
        Message(type='line', data='bye...', name='web1', color='red'),
        '',
        True,
        ' web1   | bye...'
    ),
    (
        Message(type='line', data='bye...', name='web1'),
        None,
        True,
        '13:01:13 web1   | bye...'
    ),
    (
        Message(type='line', data='bye...', name='web1'),
        "%b %d %Y %H:%M:%S",
        True,
        'Jan 17 2019 13:01:13 web1   | bye...'
    ),
    (
        Message(type='line', data='bye...', name='web1'),
        None,
        False,
        'bye...'
    ),
    (
        Message(type='line', data=b'\x28', name='web1'),
        '',
        True,
        ' web1   | ('
    ),
    (
        Message(type='line', data='bye...', name=None),
        "%H:%M:%S",
        True,
        '13:01:13        | bye...'
    ),
])
def test_write(timezone_fixture, message, time_format, use_prefix, expect):
    # Adjust message time here to use timezone_fixture settings
    message.time = datetime.fromtimestamp(1547730073)
    w = StoreWriter()
    p = Printer(w, time_format=time_format, use_prefix=use_prefix)
    s1 = Service(name='123456', cmd='cat')
    p.adjust_width(s1)
    p.write(message)
    assert expect == w.data
