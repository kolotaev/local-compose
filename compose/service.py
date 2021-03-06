import subprocess
import shlex
import os

from .system import OS
from .readiness import Readiness


class Service(object):
    '''
    Long running (daemon) process that is not expected to exit by itself.
    '''
    def __init__(self, name, cmd, color=None, quiet=False,
                 env=None, cwd=None, shell=False,
                 readiness=None, log_to_file=None):
        self.name = name
        self.cmd = cmd
        self.color = color
        self.quiet = quiet
        self.env = self._stringify_env(env)
        if cwd is None:
            # todo - move to config
            cwd = os.getcwd()
        self.cwd = cwd
        self.log_to_file = log_to_file
        self.in_shell = shell
        self._os = OS()
        self.pid = None
        self.readiness = Readiness(readiness)

    def run(self):
        '''
        Run service as the OS process.
        '''
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
        '''
        Stop OS process that represents the service.
        '''
        if force:
            self._os.kill_pid(self.pid)
        else:
            self._os.terminate_pid(self.pid)

    @staticmethod
    def _stringify_env(env):
        stringed_env = {}
        if env is None:
            return None
        for k, v in env.items():
            stringed_env[k] = str(v)
        return stringed_env


class Job(Service):
    '''
    Short running process that is expected to exit by itself.
    *Not currently used.*
    '''
