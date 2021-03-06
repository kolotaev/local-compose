from mock import Mock, patch

from compose.runtime import Executor
from compose.service import Service
from compose.messaging import EventBus, EmptyBus


def test_executor_name():
    eb = EventBus()
    srv = Service(name='web1', cmd='fake')
    executor = Executor(eb, srv)
    executor.start()
    assert executor.name == 'web1'


@patch('compose.runtime.threading.Thread')
def test_full_circle(thread_mock):
    # Process mocks
    stdout_mock = Mock()
    stdout_mock.readline.side_effect = ['webserver listens on :80', 'bye', b'']
    popen_mock = Mock(pid=3333, stdout=stdout_mock, returncode=2)
    # Service mocks
    srv = Service(name='web1', cmd='fake', quiet=False)
    srv_run_mock = Mock()
    srv_stop_mock = Mock()
    srv_run_mock.return_value = popen_mock
    srv.run = srv_run_mock
    srv.stop = srv_stop_mock
    # Create
    eb = EventBus()
    executor = Executor(eb, srv)
    # Thread mocks (a little hack to not execute in a separate thread)
    thread_obj_mock = Mock()
    thread_obj_mock.start.side_effect = executor._run_service
    thread_mock.return_value = thread_obj_mock
    # state assertions
    assert executor.child_pid is None
    assert executor.returncode is None
    # Start
    executor.start()
    # state assertions
    assert executor.child_pid == 3333
    # call assertions
    srv_run_mock.assert_called_once_with()
    stdout_mock.close.assert_called_once_with()
    popen_mock.wait.assert_called_once_with()
    # message assertions
    assert 'starting service web1' in eb.receive().data
    assert eb.receive().data == {'pid': 3333}
    assert eb.receive().data == 'webserver listens on :80'
    assert eb.receive().data == 'bye'
    assert eb.receive().data == {'returncode': 2}
    assert isinstance(eb.receive(), EmptyBus)
    # Stop
    executor.stop(force=True)
    # state assertions
    assert executor.child_pid == 3333
    assert executor.returncode == 2
    # call assertions
    srv.stop.assert_called_once_with(force=True)
    # message assertions
    assert 'stopping service web1 (pid=3333) forcefully' in eb.receive().data
    assert isinstance(eb.receive(), EmptyBus)
