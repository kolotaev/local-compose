import os
import signal

import pytest

from compose.service import Service
from compose.system import OS


class TestService(object):
    def setup_method(self, method):
        self.procs = []

    def teardown_method(self, method):
        for p in self.procs:
            if p and p.pid:
                os.kill(p.pid, signal.SIGKILL)

    def mark_service(self, proc):
        self.procs.append(proc)

    def test_run(self):
        s = Service(name='info', cmd='echo "OK"')
        proc = s.run()
        self.mark_service(proc)
        res = ''
        for line in iter(proc.stdout.readline, b''):
            res += line.decode('ascii')
        proc.stdout.close()
        assert s.pid is not None
        assert 'OK\n' == res

    def test_run_uses_env(self):
        s = Service(name='info', cmd='echo $FOO $BAR', shell=True, env={'FOO': '123', 'BAR': 'aa'})
        proc = s.run()
        self.mark_service(proc)
        res = ''
        for line in iter(proc.stdout.readline, b''):
            res += line.decode('ascii')
        proc.stdout.close()
        assert s.pid is not None
        assert '123 aa\n' == res

    def test_run_uses_cwd(self):
        s = Service(name='info', cmd='pwd', cwd='/usr/bin')
        proc = s.run()
        self.mark_service(proc)
        res = ''
        for line in iter(proc.stdout.readline, b''):
            res += line.decode('ascii')
        proc.stdout.close()
        assert s.pid is not None
        assert '/usr/bin\n' == res

    def test_run_does_not_use_shell_if_said_so(self):
        s = Service(name='info', cmd='echo $FOO $BAR',
                    env={'FOO': '123', 'BAR': 'aa'},
                    shell=False)
        proc = s.run()
        self.mark_service(proc)
        res = ''
        for line in iter(proc.stdout.readline, b''):
            res += line.decode('ascii')
        proc.stdout.close()
        assert s.pid is not None
        assert '$FOO $BAR\n' == res

    @pytest.mark.parametrize(
        'force',
        [
            False,
            True,
        ]
    )
    def test_stop(self, force):
        os = OS()
        s = Service(name='web1', cmd='nc -l 9977', shell=False)
        proc = s.run()
        self.mark_service(proc)
        assert s.pid is not None
        assert 0 != len(os.pid_by_name('nc -l 9977'))
        s.stop(force=force)
        assert 0 == len(os.pid_by_name('nc -l 9977'))
