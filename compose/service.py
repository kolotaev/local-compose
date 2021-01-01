import subprocess
import shlex
import os

from .system import OS


class Service(object):
    '''
    Long running (daemon) process that is not expected to exit by itself.
    '''
    def __init__(self, name, cmd, color=None, quiet=False, env=None, cwd=None, shell=False, readiness=None):
        self.name = name
        self.cmd = cmd
        self.color = color
        self.quiet = quiet
        self.env = env
        self.cwd = self._calculate_work_dir(cwd)
        self.in_shell = shell
        self._os = OS()
        self.pid = None
        if readiness is None:
            readiness = {}
        self.readiness = {
            'probe': readiness.get('probe'),
            'retry': RetryLogic(readiness.get('retry')['attempts'], readiness.get('retry')['wait']),
        }

    def run(self):
        if not self.in_shell:
            command = shlex.split(self.cmd)
        else:
            command = self.cmd
        proc = subprocess.Popen(command,
                                env=self.env,
                                cwd=self.cwd,
                                shell=self.in_shell,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                # todo - breaks on py27
                                # start_new_session=True,
                                close_fds=True)
        self.pid = proc.pid
        return proc

    def stop(self, force=False):
        if force:
            self._os.kill_pid(self.pid)
        else:
            self._os.terminate_pid(self.pid)

    @staticmethod
    def _calculate_work_dir(work_dir):
        if work_dir is None:
            return os.getcwd()
        return os.path.realpath(os.path.expanduser(work_dir))


class Job(Service):
    '''
    Short running process that is expected to exit by itself.
    *Not currently used.*
    '''
    pass


class RetryLogic(object):
    def __init__(self, attempts, wait):
        self._done_attempts = 0
        self.attempts = attempts
        self.wait = wait

    def do_retry(self):
        if self._done_attempts < self.attempts:
            self._done_attempts += 1
            return True
        return False
