# -*- coding: utf-8 -*-
import time

from compose.messaging import Line, Stop
from compose.utils import now


def test_message_defaults():
    m = Line(u'hello it is me на русском', 'web1')
    assert m.data == u'hello it is me на русском'
    assert m.name == 'web1'
    assert m.time <= now()
    assert m.color is None


def test_message_time():
    n = now()
    time.sleep(0.01)
    m = Line('hello', 'web1')
    time.sleep(0.01)
    m_next = Line('hello', 'web2')
    assert n < m.time
    assert m.time != m_next.time
    n2 = now()
    time.sleep(0.01)
    m2 = Line('hello2', 'web2', time=n2)
    assert m2.time == n2


def test_message_properties():
    my_time = now()
    data = '''
        multi
        line
        string
    '''
    m = Stop(data, 'web1', time=my_time, color='red')
    assert m.data == data
    assert m.name == 'web1'
    assert m.time == my_time
    assert m.color == 'red'
