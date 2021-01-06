import os
import errno
import signal
import subprocess


class OS(object):
    '''
    Helper class for operating system proxies and utilities.
    '''
    def __init__(self):
        self._type = 'unix'

    def terminate_pid(self, pid):
        '''
        Stop process with SIGTERM by its PID.
        '''
        self._kill(pid, signal.SIGTERM)

    def kill_pid(self, pid):
        '''
        Stop process with SIGKILL by its PID.
        '''
        self._kill(pid, signal.SIGKILL)

    @staticmethod
    def pid_by_name(name):
        '''
        Get PID by the process name (or the process' name representation in the shell).
        '''
        child = subprocess.Popen(['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
        response = child.communicate()[0]
        return [int(pid) for pid in response.split()]

    @staticmethod
    def _kill(pid, sig):
        try:
            os.kill(pid, sig)
        except OSError as e:
            if e.errno not in [errno.EPERM, errno.ESRCH]:
                raise
