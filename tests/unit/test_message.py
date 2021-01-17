# -*- coding: utf-8 -*-
import time

from compose.printing import MessageOutput, MessageStop
from compose.utils import now


def test_message_defaults():
    m = MessageOutput(u'hello it is me на русском', 'web1')
    assert u'hello it is me на русском' == m.data
    assert 'web1' == m.name
    assert m.time <= now()
    assert m.color is None


def test_message_time():
    n = now()
    time.sleep(0.01)
    m = MessageOutput('hello', 'web1')
    time.sleep(0.01)
    m_next = MessageOutput('hello', 'web2')
    assert n < m.time
    assert m.time != m_next.time
    n2 = now()
    time.sleep(0.01)
    m2 = MessageOutput('hello2', 'web2', time=n2)
    assert n2 == m2.time


def test_message_properties():
    my_time = now()
    data = '''
        multi
        line
        string
    '''
    m = MessageStop(data, 'web1', time=my_time, color='red')
    assert data == m.data
    assert 'web1' == m.name
    assert my_time == m.time
    assert 'red' == m.color
