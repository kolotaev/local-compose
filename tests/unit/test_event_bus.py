from compose.messaging import EventBus, EmptyBus, Line


def test_receive():
    eb = EventBus()
    msg = eb.receive(timeout=0.001)
    assert isinstance(msg, EmptyBus)
    assert msg.data == 'No messages in queue'
    assert msg.name == 'system'


def test_send_and_receive():
    eb = EventBus()
    eb.send(Line('hello it is Beth', 'web1'))
    eb.send(Line('hello it is John', 'web1'))
    msg1 = eb.receive(timeout=0.001)
    assert isinstance(msg1, Line)
    assert msg1.name == 'web1'
    assert msg1.data == 'hello it is Beth'
    msg2 = eb.receive()
    assert isinstance(msg2, Line)
    assert msg2.name == 'web1'
    assert msg2.data == 'hello it is John'
    msg3 = eb.receive()
    assert isinstance(msg3, EmptyBus)
    assert msg3.data == 'No messages in queue'
    assert msg3.name == 'system'


def test_send_system():
    eb = EventBus()
    eb.send_system('some custom system message')
    msg = eb.receive()
    assert isinstance(msg, Line)
    assert msg.data == 'some custom system message'
    assert msg.name == 'system'
