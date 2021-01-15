import threading
import signal
import datetime
try:
    import queue
except ImportError:
    import Queue as queue

from .printing import Message
from .utils import now


class Executor(object):
    '''
    Runs, re-runs, stops services.
    Each executor is associated with exactly one service.
    '''
    def __init__(self, event_bus, service):
        self.event_bus = event_bus
        self._srv = service
        self.name = service.name
        self.returncode = None
        self.child_pid = None

    def start(self):
        '''
        Start thread for execution of the underlying service.
        '''
        self.event_bus.send_system('starting service {s}'.format(s=self._srv.name))
        th = threading.Thread(name=self.name, target=self._run_service)
        th.start()

    def stop(self, force=False):
        '''
        Stop thread for execution of the underlying service.
        '''
        kill_type = 'forcefully' if force else 'gracefully'
        msg = 'stopping service {name} (pid={pid}) {method}\n'. \
                format(method=kill_type, name=self._srv.name, pid=self.child_pid)
        self.event_bus.send_system(msg)
        self._srv.stop(force=force)

    def reset(self):
        '''
        Reset return code of the service.
        '''
        self.returncode = None

    def _run_service(self):
        child = self._srv.run()
        self.child_pid = child.pid
        self._send_message({'pid': self.child_pid}, 'start')
        for line in iter(child.stdout.readline, b''):
            if not self._srv.quiet:
                self._send_message(line, 'output')
        child.stdout.close()
        child.wait()
        self._send_message({'returncode': child.returncode}, 'stop')
        self.returncode = child.returncode

    def _send_message(self, data, msg_type):
        self.event_bus.send(Message(type=msg_type, data=data, name=self._srv.name, color=self._srv.color))


class EventBus():
    '''
    Main event messaging bus for the runtime.
    '''
    def __init__(self):
        self._bus = queue.Queue()

    def receive(self, timeout=0.1):
        '''
        Receive a message from this event bus.
        '''
        try:
            return self._bus.get(timeout=timeout)
        except queue.Empty:
            return Message(type='no_messages', data='No messages in queue', name='system')

    def send(self, message):
        '''
        Send a message to this event bus.
        '''
        self._bus.put(message)

    def send_system(self, data, type='output'):
        '''
        Send a system-type message to this event bus.
        '''
        self._bus.put(Message(type=type, data=data, name='system'))


class ExecutorsPool(object):
    '''
    Pooled collection of executors.
    '''
    def __init__(self):
        self._executors = {}

    def add(self, executor):
        '''
        Add executor to pool.
        '''
        self._executors[executor.name] = executor

    def get(self, name):
        '''
        Get executor from pool.
        '''
        return self._executors.get(name)

    def all(self):
        '''
        Get all executors from pool.
        '''
        return self._executors.values()

    def start_all(self):
        '''
        Start all executors in the pool.
        '''
        for executor in self.all():
            executor.start()

    def stop_all(self, force=False):
        '''
        Stop all executors in the pool. Unless they already haven't exited by themselves.
        '''
        for executor in self.all():
            if executor.returncode is None:
                executor.stop(force)

    def all_started(self):
        '''
        Are all executors started?
        '''
        return all(e.child_pid is not None for e in self.all())

    def all_stopped(self):
        '''
        Are all executors stopped?
        '''
        return all(e.returncode is not None for e in self.all())


class Supervisor(object):
    '''
    Supervises status, execution, readiness of services and jobs.
    '''
    def __init__(self, event_bus, exec_pool):
        self.name = 'local_compose_supervisor'
        self.eb = event_bus
        self.exec_pool = exec_pool
        self._event = threading.Event()
        self._stop = False

    def launch(self):
        '''
        Start supervision.
        '''
        th = threading.Thread(name=self.name, target=self.monitor)
        th.start()

    def stop(self):
        '''
        Stop supervision.
        '''
        self._stop = True
        self._event.set()

    def monitor(self):
        '''
        The actual supervision method.
        '''
        while True:
            if self._stop:
                break
            for executor in self.exec_pool.all():
                if self.needs_restart(executor):
                    self._event.wait(10)
                    executor.reset()
                    self.eb.send_system(type='restart', data={'name': executor.name})

    # todo - move to executor
    def needs_restart(self, executor):
        '''
        Must executor be restarted?
        '''
        rc = executor.returncode
        if rc is not None and rc != 0:
            return True
        return False


class Scheduler(object):
    '''
    Manager for scheduling, running, stopping and monitoring services.
    '''
    def __init__(self, printer, kill_wait=5):
        self.event_bus = EventBus()
        # todo - set it correctly
        self.returncode = None
        self.kill_wait = kill_wait
        self._printer = printer
        self._pool = ExecutorsPool()
        self._supervisor = Supervisor(self.event_bus, self._pool)
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

    def register_service(self, service):
        '''
        Register Service within the Scheduler.
        '''
        executor = Executor(self.event_bus, service)
        self._pool.add(executor)
        self._printer.adjust_width(service)

    def start(self):
        '''
        Start the main managing and execution logic of the Scheduler.
        '''
        def _terminate(signum, frame):
            self.event_bus.send_system('%s received\n' % self.signals[signum]['name'])
            self.returncode = self.signals[signum]['rc']
            self.terminate()

        signal.signal(signal.SIGTERM, _terminate)
        signal.signal(signal.SIGINT, _terminate)

        self._pool.start_all()
        self._supervisor.launch()

        do_exit = False
        exit_start = None

        while True:
            msg = self.event_bus.receive(timeout=0.1)
            if msg.type == 'no_messages' and do_exit:
                break
            if msg.type == 'output':
                self._printer.write(msg)
            elif msg.type == 'start':
                pid = msg.data['pid']
                self.event_bus.send_system('{name} started (pid={pid})\n'.format(name=msg.name, pid=pid))
            elif msg.type == 'restart':
                name = msg.data['name']
                self.event_bus.send_system('{name} is restarting\n'.format(name=name))
                self._pool.get(name).start()
            elif msg.type == 'stop':
                rc = msg.data['returncode']
                self.event_bus.send_system('{name} stopped (rc={rc})\n'.format(name=msg.name, rc=rc))
                if self.returncode is None:
                    self.returncode = rc

            if self._pool.all_started() and self._pool.all_stopped():
                do_exit = True
                # It will be our guard against hanging executors
                if exit_start is None:
                    exit_start = now()
                self.terminate()

            if exit_start is not None:
                # If we're running (though have triggered an exit) more than kill_wait seconds,
                # we need to kill all the hanging executors.
                waiting = now() - exit_start
                if waiting > datetime.timedelta(seconds=self.kill_wait):
                    self._kill()

    def terminate(self):
        '''
        Stop (maybe forcefully) the Scheduler.
        '''
        if self._terminating:
            return
        self._terminating = True
        self._supervisor.stop()
        self._pool.stop_all()

    def _kill(self):
        self._pool.stop_all(force=True)
