from mock import Mock

from compose.runtime import Executor, EventBus
from compose.service import Service


def test_executor_name():
    eb = EventBus()
    srv = Service(name='web1', cmd='fake')
    executor = Executor(eb, srv)
    executor.start()
    assert 'web1' == executor.name


def test_full_circle():
    stdout_mock = Mock()
    stdout_mock.readline.side_effect = ['webserver listens on :80', 'bye', '']
    popen_mock = Mock(pid=3333, stdout=stdout_mock, returncode=2)
    srv = Service(name='web1', cmd='fake', quiet=False)
    srv_run_mock = Mock()
    srv_kill_mock = Mock()
    srv_run_mock.return_value = popen_mock
    srv.run = srv_run_mock
    srv.kill = srv_kill_mock
    # Create
    eb = EventBus()
    executor = Executor(eb, srv)
    # state assertions
    assert executor.child_pid is None
    assert executor.returncode is None
    # Start
    executor.start()
    # state assertions
    assert 3333 == executor.child_pid
    # call assertions
    srv_run_mock.assert_called_once_with()
    stdout_mock.close.assert_called_once_with()
    popen_mock.wait.assert_called_once_with()
    # message assertions
    assert 'starting service web1' in eb.receive().data
    assert {'pid': 3333} == eb.receive().data
    assert 'webserver listens on :80' == eb.receive().data
    assert 'bye' == eb.receive().data
    assert {'returncode': 2} == eb.receive().data
    assert 'no_messages' == eb.receive().type
    # Stop
    executor.stop(force=True)
    # state assertions
    assert 3333 == executor.child_pid
    assert 2 == executor.returncode
    # call assertions
    srv.kill.assert_called_once_with(force=True)
    # message assertions
    assert 'stopping service web1 (pid=3333) forcefully' in eb.receive().data
    assert 'no_messages' == eb.receive().type
