import os
import signal
import subprocess

from .printing import Message
from .utils import now


class Service(object):
    def __init__(self, cmd, name=None, color=None, quiet=False, env=None, cwd=None, shell=True):
        self.cmd = cmd
        self.color = color
        self.quiet = quiet
        self.name = name
        self.env = os.environ.copy() if env is None else env
        self.cwd = cwd
        self.in_shell = shell
        self._proc = None

    def run(self, events=None, ignore_signals=False):
        self._events = events
        self._proc = subprocess.Popen(self.cmd,
                                      env=self.env,
                                      cwd=self.cwd,
                                      shell=self.in_shell,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      start_new_session=True,
                                      close_fds=True)
        self._send_message({'pid': self._proc.pid}, 'start')

        # Don't pay attention to SIGINT/SIGTERM. The process itself is
        # considered unkillable, and will only exit when its child (the shell
        # running the Procfile process) exits.
        if ignore_signals:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            signal.signal(signal.SIGTERM, signal.SIG_IGN)

        for line in iter(self._proc.stdout.readline, b''):
            if not self.quiet:
                self._send_message(line, 'line')
        self._proc.stdout.close()
        self._proc.wait()

        self._send_message({'returncode': self._proc.returncode}, 'stop')

    def _send_message(self, data, msg_type):
        if self._events is not None:
            self._events.put(Message(type=msg_type, data=data, time=now(), name=self.name, color=self.color))


class Job(Service):
    pass
