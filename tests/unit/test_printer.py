import pytest

from compose.printing import Printer, Message
from compose.service import Service


class StoreWriter(object):
    def __init__(self):
        self.data = ''

    def write(msg, color=None):
        self.data = msg


def test_printer_does_not_allow_other_mesage_types():
    w = StoreWriter()
    p = Printer(w)
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
