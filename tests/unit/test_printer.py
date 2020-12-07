import pytest

from compose.printing import Printer, Message


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
