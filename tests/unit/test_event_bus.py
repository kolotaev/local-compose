from compose.runtime import EventBus
from compose.printing import Message


def test_receive():
    eb = EventBus()
    msg = eb.receive(timeout=0.001)
    assert 'no_messages' == msg.type
    assert 'No messages in queue' == msg.data
    assert 'system' == msg.name


def test_send_and_receive():
    eb = EventBus()
    eb.send(Message('output', 'hello it is Beth', 'web1'))
    eb.send(Message('output', 'hello it is John', 'web1'))
    msg1 = eb.receive(timeout=0.001)
    assert 'output' == msg1.type
    assert 'web1' == msg1.name
    assert 'hello it is Beth' == msg1.data
    msg2 = eb.receive()
    assert 'output' == msg2.type
    assert 'web1' == msg2.name
    assert 'hello it is John' == msg2.data
    msg3 = eb.receive()
    assert 'no_messages' == msg3.type
    assert 'No messages in queue' == msg3.data
    assert 'system' == msg3.name


def test_send_system():
    eb = EventBus()
    eb.send_system('some custom system message')
    msg = eb.receive()
    assert 'output' == msg.type
    assert 'some custom system message' == msg.data
    assert 'system' == msg.name
