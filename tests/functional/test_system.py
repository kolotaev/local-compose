import os
import signal

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
        pid = self.launch_service(program)
        pids_found = OS().pid_by_name(program)
        assert len(pids_found) > 0
        assert pids_found[0] == pid

    @pytest.mark.parametrize(
        'program, in_shell',
        [
            ('nc -l 9991', False),
            ('while true; do echo "hello"; done', True),
        ]
    )
    def test_kill_pid(self, program, in_shell):
        pid = self.launch_service(program, shell=in_shell)
        assert len(OS().pid_by_name(program)) == 1
        OS().kill_pid(pid)
        assert len(OS().pid_by_name(program)) == 0

    @pytest.mark.parametrize(
        'program, in_shell',
        [
            ('nc -l 9992', False),
            ('while true; do echo "hello"; done', True),
        ]
    )
    def test_terminate_pid(self, program, in_shell):
        pid = self.launch_service(program, shell=in_shell)
        assert len(OS().pid_by_name(program)) == 1
        OS().terminate_pid(pid)
        assert len(OS().pid_by_name(program)) == 0

    def test_does_not_panic_when_terminating_unknown_pid(self):
        OS().terminate_pid(99999999)

    def test_does_not_panic_when_killing_unknown_pid(self):
        OS().kill_pid(99999999)
