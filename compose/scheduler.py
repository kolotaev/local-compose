import datetime
import queue
import multiprocessing
import signal
import sys

from .printing import Message
from .execution import Executor, Pool
from .service import Service
from .utils import now


KILL_WAIT = 3
SYSTEM_PRINTER_NAME = 'system'
SIGNALS = {
    signal.SIGINT: {
        'name': 'SIGINT',
        'rc': 130,
    },
    signal.SIGTERM: {
        'name': 'SIGTERM',
        'rc': 143,
    },
}


class Scheduler(object):
    returncode = None

    def __init__(self, printer, os):
        self.events = multiprocessing.Queue()
        self.returncode = None
        self._printer = printer
        self._pool = Pool()
        self._os = os
        self._terminating = False

    def add_service(self, name, cmd, color, quiet=False, env=None, cwd=None):
        srv = Service(cmd, name=name, quiet=quiet, color=color, env=env, cwd=cwd)
        executor = Executor(self.events, srv, self._os)
        self._pool.add(executor)
        self._printer.width = max(self._printer.width, len(name))

    def start(self):
        def _terminate(signum, frame):
            self._system_print('%s received\n' % SIGNALS[signum]['name'])
            self.returncode = SIGNALS[signum]['rc']
            self.terminate()

        signal.signal(signal.SIGTERM, _terminate)
        signal.signal(signal.SIGINT, _terminate)

        self._pool.start_all()

        exit = False
        exit_start = None

        while True:
            try:
                msg = self.events.get(timeout=0.1)
            except queue.Empty:
                if exit:
                    break
            else:
                if msg.type == 'line':
                    self._printer.write(msg)
                elif msg.type == 'start':
                    pid = msg.data['pid']
                    self._pool.set_pid(msg.name, pid)
                    self._system_print('{name} started (pid={pid})\n'.format(name=msg.name, pid=pid))
                elif msg.type == 'stop':
                    rc = msg.data['returncode']
                    self._pool.set_rc(msg.name, rc)
                    self._system_print('{name} stopped (rc={rc})\n'.format(name=msg.name, rc=rc))
                    if self.returncode is None:
                        self.returncode = rc

            if self._pool.all_started() and self._pool.all_stopped():
                exit = True

            if exit_start is None and self._pool.all_started() and self._pool.any_stopped():
                exit_start = now()
                self.terminate()

            if exit_start is not None:
                # If we've been in this loop for more than KILL_WAIT seconds,
                # it's time to kill all remaining children.
                waiting = now() - exit_start
                if waiting > datetime.timedelta(seconds=KILL_WAIT):
                    self.kill()

    def terminate(self):
        if self._terminating:
            return
        self._terminating = True
        self._pool.stop_all()

    def kill(self):
        self._pool.stop_all(force=True)

    def _system_print(self, data):
        self._printer.write(Message(type='line', data=data, time=now(), name=SYSTEM_PRINTER_NAME, color=None))
