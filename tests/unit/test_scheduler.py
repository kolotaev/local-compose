from mock import Mock, patch

from compose.runtime import Scheduler
from compose.service import Service
from compose.printing import Message


def test_ctor():
    printer = Mock()
    sch = Scheduler(printer, 10)
    sch.add_service(Service(name='web1', cmd='fake'))
    assert sch.returncode is None
    assert 10 == sch.kill_wait
    sch2 = Scheduler(printer)
    assert sch2.returncode is None
    assert 5 == sch2.kill_wait


def test_add_service():
    printer = Mock()
    sch = Scheduler(printer)
    sch.add_service(Service(name='web1', cmd='fake'))
    sch.add_service(Service(name='web2', cmd='fake'))
    assert sch.returncode is None
    assert 2 == len(sch._pool.all())


# @patch('compose.runtime.EventBus')
# @patch('compose.runtime.ExecutorsPool')
# def test_start_no_messages(eb_cls, pool_cls):
#     eb = Mock()
#     eb_cls.side_effect = eb
#     eb.receive.side_effect = [
#         Message(type='no_messages', data='nothing here', name='system'),
#     ]
#     pool = Mock()
#     pool.all_started.return_value = True
#     pool.all_stopped.return_value = True
#     pool_cls.side_effect = pool
#     printer = Mock()
#     sch = Scheduler(printer)
#     sch.start()
#     pool.start_all.assert_called_once()