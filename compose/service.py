import subprocess
import shlex

from .system import OS


class Service(object):
    '''
    Long running (daemon) process that is not expected to exit by itself.
    '''
    def __init__(self, name, cmd, color=None, quiet=False, env=None, cwd=None, shell=True):
        self.name = name
        self.cmd = cmd
        self.color = color
        self.quiet = quiet
        self.env = env
        self.cwd = cwd
        self.in_shell = shell
        self._os = OS()
        self.pid = None

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

class Job(Service):
    '''
    Short running process that is expected to exit by itself.
    '''
    pass
