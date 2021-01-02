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
        self._kill(pid, signal.SIGTERM)

    def kill_pid(self, pid):
        self._kill(pid, signal.SIGKILL)

    def pid_by_name(self, name):
        child = subprocess.Popen(['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
        response = child.communicate()[0]
        return [int(pid) for pid in response.split()]

    def _kill(self, pid, sig):
        try:
            os.kill(pid, sig)
        except OSError as e:
            if e.errno not in [errno.EPERM, errno.ESRCH]:
                raise
