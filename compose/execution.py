import os
# import signal
import subprocess
import threading

from .printing import Message
from .utils import now


class Executor(object):
    def __init__(self, events, service, os):
        self._events = events
        self._srv = service
        self._os = os
        self.name = service.name
        self.returncode = None
        self.child_pid = None

    def start(self):
        proc = threading.Thread(name=self.name, target=self._run_service, args=(True, ))
        proc.start()

    def stop(self, force=False):
        sig = 'SIGKILL' if force else 'SIGTERM'
        msg = 'about to get {signal} from System\n'.format(signal=sig)
        self._send_message(msg, 'line')
        if force:
            self._os.kill_pid(self.child_pid)
        else:
            self._os.terminate_pid(self.child_pid)

    def _run_service(self, ignore_signals=False):
        child = self._srv.run()
        self.child_pid = child.pid
        self._send_message({'pid': self.child_pid}, 'start')

        for line in iter(child.stdout.readline, b''):
            if not self._srv.quiet:
                self._send_message(line, 'line')
        child.stdout.close()
        child.wait()

        self._send_message({'returncode': child.returncode}, 'stop')
        self.returncode = child.returncode

    def _send_message(self, data, msg_type):
        self._events.put(Message(type=msg_type, data=data, time=now(), name=self._srv.name, color=self._srv.color))


class Pool(object):
    def __init__(self):
        self._executors = {}

    def add(self, executor):
        self._executors[executor.name] = executor

    def all(self):
        return self._executors.items()

    def get(self, name):
        return self._executors.get(name)

    def start_all(self):
        for i, executor in self.all():
            executor.start()

    def stop_all(self, force=False):
        for _, p in self.all():
            if p.returncode is None:
                p.stop(force)

    def all_started(self):
        return all(p.child_pid is not None for _, p in self.all())

    def all_stopped(self):
        return all(p.returncode is not None for _, p in self.all())

    def any_stopped(self):
        return any(p.returncode is not None for _, p in self.all())
