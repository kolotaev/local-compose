import os
import errno
import sys
import signal
import subprocess
import tempfile
import shutil
import hashlib

from .info import NAME


if sys.version_info[0] == 2:
    class FileExistsError(OSError):
        def __init__(self, msg):
            super(FileExistsError, self).__init__(errno.EEXIST, msg)


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
    '''
    Manages data related to compose invocation:
    - Creates/removes a temporary directory
    - Creates/removes file with the invocation's PID
    - Related data retrieval
    Each Storage object is bound to a specific config file name (and thus invocation).
    '''
    def __init__(self, config_filepath):
        box = hashlib.md5()
        box.update(config_filepath.encode('utf-8'))
        self._tempdir = os.path.join(tempfile.gettempdir(), NAME, box.hexdigest())
        self._pidfile = os.path.join(self._tempdir, 'run.pid')

    def get_tempdir_name(self):
        '''
        Get name of the tempdir this storage is bound to.
        '''
        return self._tempdir

    def prepare_tempdir(self):
        '''
        Possibly create a temp directory for this compose run.
        We'll use it to store PIDs, logs, etc.
        '''
        try:
            # todo - fix
            os.makedirs(self._tempdir)
        except FileExistsError:
            pass

    def clean_tempdir(self):
        '''
        Delete a temp directory for this compose run.
        '''
        shutil.rmtree(self._tempdir, ignore_errors=True)

    def pid_exists(self):
        '''
        Does file with PID exist?
        '''
        return os.path.isfile(self._pidfile)

    def create_pid(self):
        '''
        Create file with the invocation's PID.
        '''
        own_pid = os.getpid()
        with open(self._pidfile, 'w') as f:
            f.write(str(own_pid))

    def pid_read(self):
        '''
        Read invocation's PID from file.
        '''
        with open(self._pidfile, 'r') as f:
            data = f.read()
            return int(data)
