from mock import Mock

from compose.runtime import Scheduler
from compose.service import Service


def test_ctor():
    printer = Mock()
    sch = Scheduler(printer, 10)
    sch.register_service(Service(name='web1', cmd='fake'))
    assert sch.returncode is None
    assert sch.kill_wait == 10
    sch2 = Scheduler(printer)
    assert sch2.returncode is None
    assert sch2.kill_wait == 5


def test_register_service():
    printer = Mock()
    sch = Scheduler(printer)
    sch.register_service(Service(name='web1', cmd='fake'))
    sch.register_service(Service(name='web2', cmd='fake'))
    assert sch.returncode is None
    assert len(sch._pool.all()) == 2
