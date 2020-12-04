import os
import signal
import time

import pytest

from compose.system import OS
from compose.service import Service


class TestOS(object):
    def setup_method(self, method):
        self.procs = []

    def teardown_method(self, method):
        for p in self.procs:
            if p and p.pid:
                os.kill(p.pid, signal.SIGKILL)

    def launch_service(self, cmd, shell=False):
        srv = Service('local-compose-test-program', cmd, shell=shell)
        proc = srv.run()
        self.procs.append(proc)
        assert proc.pid
        return proc.pid

    def test_get_pid_by_name(self):
        program = 'nc -l 9990'
        os = OS()
        pid = self.launch_service(program)
        pids_found = os.pid_by_name(program)
        assert len(pids_found) > 0
        assert pid == pids_found[0]

    @pytest.mark.parametrize(
        'program, in_shell',
        [
            ('nc -l 9991', False),
            ('while true; do echo "hello"; done', True),
        ]
    )
    def test_kill_pid(self, program, in_shell):
        os = OS()
        pid = self.launch_service(program, shell=in_shell)
        assert 1 == len(os.pid_by_name(program))
        os.kill_pid(pid)
        assert 0 == len(os.pid_by_name(program))

    @pytest.mark.parametrize(
        'program, in_shell',
        [
            ('nc -l 9992', False),
            ('while true; do echo "hello"; done', True),
        ]
    )
    def test_terminate_pid(self, program, in_shell):
        os = OS()
        pid = self.launch_service(program, shell=in_shell)
        assert 1 == len(os.pid_by_name(program))
        os.terminate_pid(pid)
        assert 0 == len(os.pid_by_name(program))
