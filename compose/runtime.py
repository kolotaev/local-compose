import threading
import queue
import signal
import datetime

from .printing import Message
from .utils import now


class Executor(object):
    def __init__(self, event_bus, service, os):
        self.event_bus = event_bus
        self._srv = service
        self._os = os
        self.name = service.name
        self.returncode = None
        self.child_pid = None

    def start(self):
        th = threading.Thread(name=self.name, target=self._run_service, args=(True, ))
        th.start()

    def stop(self, force=False):
        sig = 'SIGKILL' if force else 'SIGTERM'
        msg = 'sending {signal} to {name}(pid={pid})\n'.format(signal=sig, name=self._srv.name, pid=self.child_pid)
        self.event_bus.send_system(msg)
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
        self.event_bus.send(Message(type=msg_type, data=data, name=self._srv.name, color=self._srv.color))


class EventBus():
    def __init__(self):
        self._bus = queue.Queue()

    def receive(self, timeout):
        try:
            return self._bus.get(timeout=timeout)
        except queue.Empty:
            return Message(type='no_messages', data='No messages in queue', name='system')

    def send(self, message):
        self._bus.put(message)

    def send_system(self, text):
        self._bus.put(Message(type='line', data=text, name='system'))


class ExecutorsPool(object):
    def __init__(self):
        self._executors = {}

    def add(self, executor):
        self._executors[executor.name] = executor

    def get(self, name):
        return self._executors.get(name)

    def all(self):
        return self._executors.items()

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


class Scheduler(object):
    returncode = None

    def __init__(self, printer, os, kill_wait=5):
        self.event_bus = EventBus()
        self.returncode = None
        self.kill_wait = kill_wait
        self._printer = printer
        self._pool = ExecutorsPool()
        self._os = os
        self._terminating = False
        self.signals = {
            signal.SIGINT: {
                'name': 'SIGINT',
                'rc': 130,
            },
            signal.SIGTERM: {
                'name': 'SIGTERM',
                'rc': 143,
            },
        }

    def add_service(self, service):
        executor = Executor(self.event_bus, service, self._os)
        self._pool.add(executor)
        self._printer.adjust_width(service)

    def start(self):
        def _terminate(signum, frame):
            self.event_bus.send_system('%s received\n' % self.signals[signum]['name'])
            self.returncode = self.signals[signum]['rc']
            self.terminate()

        signal.signal(signal.SIGTERM, _terminate)
        signal.signal(signal.SIGINT, _terminate)

        self._pool.start_all()

        do_exit = False
        exit_start = None

        while True:
            msg = self.event_bus.receive(timeout=0.1)
            if msg.type == 'no_messages' and do_exit:
                break
            if msg.type == 'line':
                self._printer.write(msg)
            elif msg.type == 'start':
                pid = msg.data['pid']
                self.event_bus.send_system('{name} started (pid={pid})\n'.format(name=msg.name, pid=pid))
            elif msg.type == 'stop':
                rc = msg.data['returncode']
                self.event_bus.send_system('{name} stopped (rc={rc})\n'.format(name=msg.name, rc=rc))
                if self.returncode is None:
                    self.returncode = rc

            if self._pool.all_started() and self._pool.all_stopped():
                do_exit = True

            if exit_start is None and self._pool.all_started() and self._pool.any_stopped():
                exit_start = now()
                self.terminate()

            if exit_start is not None:
                # If we've been in this loop for more than kill_wait seconds,
                # it's time to kill all remaining children.
                waiting = now() - exit_start
                if waiting > datetime.timedelta(seconds=self.kill_wait):
                    self.kill()

    def terminate(self):
        if self._terminating:
            return
        self._terminating = True
        self._pool.stop_all()

    def kill(self):
        self._pool.stop_all(force=True)