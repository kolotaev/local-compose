from mock import Mock, patch

from compose.runtime import Scheduler
from compose.service import Service
from compose.printing import Message


def test_ctor():
    printer = Mock()
    sch = Scheduler(printer, 10)
    sch.register_service(Service(name='web1', cmd='fake'))
    assert sch.returncode is None
    assert 10 == sch.kill_wait
    sch2 = Scheduler(printer)
    assert sch2.returncode is None
    assert 5 == sch2.kill_wait


def test_register_service():
    printer = Mock()
    sch = Scheduler(printer)
    sch.register_service(Service(name='web1', cmd='fake'))
    sch.register_service(Service(name='web2', cmd='fake'))
    assert sch.returncode is None
    assert 2 == len(sch._pool.all())
