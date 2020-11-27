import os
import signal
import subprocess
import multiprocessing

from .printing import Message
from .utils import now

class Executor(object):
    def __init__(self, events, service, os):
        self._events = events
        self._srv = service
        self._os = os
        self.name = service.name
        self.returncode = None
        self.pid = None

    def start(self):
        proc = multiprocessing.Process(name=self.name, target=self._run_service, args=(True, ))
        proc.start()

    def stop(self, force=False):
        sig = 'SIGKILL' if force else 'SIGTERM'
        msg = 'about to get {signal} from System\n'.format(signal=sig)
        self._send_message(msg, 'line')
        if force:
            self._os.kill_pid(self.pid)
        else:
            self._os.terminate_pid(self.pid)

    def _run_service(self, ignore_signals=False):
        child = self._srv.run()
        self._send_message({'pid': child.pid}, 'start')

        # Don't pay attention to SIGINT/SIGTERM. The process itself is
        # considered unkillable, and will only exit when its child (the shell
        # running the Service process) exits.
        if ignore_signals:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            signal.signal(signal.SIGTERM, signal.SIG_IGN)

        for line in iter(child.stdout.readline, b''):
            if not self._srv.quiet:
                self._send_message(line, 'line')
        child.stdout.close()
        child.wait()

        self._send_message({'returncode': child.returncode}, 'stop')

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

    def set_rc(self, name, returncode):
        self.get(name).returncode = returncode

    def set_pid(self, name, pid):
        self.get(name).pid = pid

    def start_all(self):
        for i, executor in self.all():
            executor.start()

    def stop_all(self, force=False):
        for _, p in self.all():
            if p.returncode is None:
                p.stop(force)

    def all_started(self):
        return all(p.pid is not None for _, p in self.all())

    def all_stopped(self):
        return all(p.returncode is not None for _, p in self.all())

    def any_stopped(self):
        return any(p.returncode is not None for _, p in self.all())
