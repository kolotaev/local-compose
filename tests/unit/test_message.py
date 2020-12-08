# -*- coding: utf-8 -*-

from compose.printing import Message
from compose.utils import now


def test_message_defaults():
    m = Message('output', u'hello it is me на русском', 'web1')
    assert 'output' == m.type
    assert u'hello it is me на русском' == m.data
    assert 'web1' == m.name
    assert m.time <= now()
    assert m.color is None


def test_message_properties():
    my_time = now()
    data = '''
        multi
        line
        string
    '''
    m = Message('stop', data, 'web1', time=my_time, color='red')
    assert 'stop' == m.type
    assert data == m.data
    assert 'web1' == m.name
    assert my_time == m.time
    assert 'red' == m.color
