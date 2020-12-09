# from mock import Mock

# from compose.runtime import Executor, EventBus
# from compose.service import Service


# def test_start():
#     eb = EventBus()
#     def run_mock():
#         return Mock(pid=123, stdout=Mock(),
#                     wait=Mock(), returncode=0)
#     s = Mock(name='web1', cmd='fake', run=run_mock)
#     executor = Executor(eb, s, Mock())
#     executor.start()
#     assert False
