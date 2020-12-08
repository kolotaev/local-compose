from mock import Mock

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
    res = list(ep.all())
    assert res[0] != res[1]
    assert res[0].returncode is None
    assert res[1].returncode is None


def test_all_empty():
    ep = ExecutorsPool()
    assert 0 == len(ep.all())


def test_start_all():
    ep = ExecutorsPool()
    e1 = Mock()
    e2 = Mock()
    ep.add(e1)
    ep.add(e2)
    ep.start_all()
    e1.start.assert_called_once()
    e2.start.assert_called_once()


def test_stop_all_force():
    ep = ExecutorsPool()
    e1 = Mock(returncode=None)
    e2 = Mock(returncode=None)
    ep.add(e1)
    ep.add(e2)
    ep.stop_all(force=True)
    e1.stop.assert_called_once_with(True)
    e2.stop.assert_called_once_with(True)


def test_stop_all_non_force():
    ep = ExecutorsPool()
    e1 = Mock(returncode=None)
    e2 = Mock(returncode=None)
    ep.add(e1)
    ep.add(e2)
    ep.stop_all()
    e1.stop.assert_called_once_with(False)
    e2.stop.assert_called_once_with(False)


def test_stop_all_not_all_have_empty_returncode():
    ep = ExecutorsPool()
    e1 = Mock(returncode=None)
    e2 = Mock(returncode=1)
    e3 = Mock(returncode=None)
    ep.add(e1)
    ep.add(e2)
    ep.add(e3)
    ep.stop_all()
    e1.stop.assert_called_once()
    e2.stop.assert_not_called()
    e3.stop.assert_called_once()


def test_all_started():
    ep = ExecutorsPool()
    e1 = Executor(EventBus, Service('web1', 'cat'), OS())
    e2 = Executor(EventBus, Service('web2', 'cat'), OS())
    ep.add(e1)
    ep.add(e2)
    e1.child_pid = 123
    e2.child_pid = 1111
    assert ep.all_started()


def test_all_started_not():
    ep = ExecutorsPool()
    e1 = Executor(EventBus, Service('web1', 'cat'), OS())
    e2 = Executor(EventBus, Service('web2', 'cat'), OS())
    ep.add(e1)
    ep.add(e2)
    e1.child_pid = 123
    assert not ep.all_started()


def test_all_stopped():
    ep = ExecutorsPool()
    e1 = Executor(EventBus, Service('web1', 'cat'), OS())
    e2 = Executor(EventBus, Service('web2', 'cat'), OS())
    ep.add(e1)
    ep.add(e2)
    e1.returncode = 1
    e2.returncode = 0
    assert ep.all_stopped()


def test_all_stopped_not():
    ep = ExecutorsPool()
    e1 = Executor(EventBus, Service('web1', 'cat'), OS())
    e2 = Executor(EventBus, Service('web2', 'cat'), OS())
    ep.add(e1)
    ep.add(e2)
    e1.returncode = 1
    assert not ep.all_stopped()


def test_any_stopped():
    ep = ExecutorsPool()
    e1 = Executor(EventBus, Service('web1', 'cat'), OS())
    e2 = Executor(EventBus, Service('web2', 'cat'), OS())
    ep.add(e1)
    ep.add(e2)
    e1.returncode = 1
    assert ep.any_stopped()


def test_any_stopped_not():
    ep = ExecutorsPool()
    e1 = Executor(EventBus, Service('web1', 'cat'), OS())
    e2 = Executor(EventBus, Service('web2', 'cat'), OS())
    ep.add(e1)
    ep.add(e2)
    assert not ep.any_stopped()
