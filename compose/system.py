import os
import errno
import signal
import subprocess
import tempfile
import shutil
import hashlib

from .info import NAME


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


class Storage(object):
    def __init__(self, workdir, filename):
        box = hashlib.md5()
        # todo - fix trailing slashes
        box.update(workdir.encode('utf-8') + filename.encode('utf-8'))
        self._tempdir = os.path.join(tempfile.gettempdir(), NAME, box.hexdigest())
        self._pidfile = os.path.join(self._tempdir, 'run.pid')

    def maybe_create_tempdir(self):
        '''
        Possible create temp directory for this program.
        We'll use it to store PIDs, logs, etc.
        '''
        try:
            # todo - fix
            os.makedirs(self._tempdir)
        except Exception:
            pass

    def clean_tempdir(self):
        shutil.rmtree(self._tempdir, ignore_errors=True)

    def pid_exists(self):
        return os.path.isfile(self._pidfile)

    def pid_create(self):
        own_pid = os.getpid()
        with open(self._pidfile, 'w') as file:
            file.write(str(own_pid))

    def pid_read(self):
        with open(self._pidfile, 'r') as file:
            data = file.read()
            return int(data)
