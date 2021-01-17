from compose.messaging import EventBus, EmptyBus, Line


def test_receive():
    eb = EventBus()
    msg = eb.receive(timeout=0.001)
    assert isinstance(msg, EmptyBus)
    assert 'No messages in queue' == msg.data
    assert 'system' == msg.name


def test_send_and_receive():
    eb = EventBus()
    eb.send(Line('hello it is Beth', 'web1'))
    eb.send(Line('hello it is John', 'web1'))
    msg1 = eb.receive(timeout=0.001)
    assert isinstance(msg1, Line)
    assert 'web1' == msg1.name
    assert 'hello it is Beth' == msg1.data
    msg2 = eb.receive()
    assert isinstance(msg2, Line)
    assert 'web1' == msg2.name
    assert 'hello it is John' == msg2.data
    msg3 = eb.receive()
    assert isinstance(msg3, EmptyBus)
    assert 'No messages in queue' == msg3.data
    assert 'system' == msg3.name


def test_send_system():
    eb = EventBus()
    eb.send_system('some custom system message')
    msg = eb.receive()
    assert isinstance(msg, Line)
    assert 'some custom system message' == msg.data
    assert 'system' == msg.name
