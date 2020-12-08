from compose.runtime import ExecutorsPool, Executor, EventBus
from compose.service import Service
from compose.system import OS


def test_add_get():
    ep = ExecutorsPool()
    e1 = Executor(EventBus, Service('web1', 'cat'), OS())
    e2 = Executor(EventBus, Service('web2', 'cat'), OS())
    e3 = Executor(EventBus, Service('web2', 'cat'), OS())
    ep.add(e1)
    ep.add(e2)
    assert e1 == ep.get('web1')
    assert e2 == ep.get('web2')
    ep.add(e3)
    assert e3 == ep.get('web2')


def test_all():
    ep = ExecutorsPool()
    e1 = Executor(EventBus, Service('web1', 'cat'), OS())
    e2 = Executor(EventBus, Service('web2', 'cat'), OS())
    ep.add(e1)
    ep.add(e2)
    assert 2 == len(ep.all())
    assert ep.all()[0] != ep.all()[1]
    assert ep.all()[0].returncode is None
    assert ep.all()[1].returncode is None


def test_start_all():
    pass
