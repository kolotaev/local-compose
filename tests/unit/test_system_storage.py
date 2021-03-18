import shutil
import os

from compose.system import Storage


class TestStorage(object):
    def setup_method(self):
        self.dirs = []

    def teardown_method(self):
        for d in self.dirs:
            shutil.rmtree(d, ignore_errors=True)

    def mark_dir(self, name):
        self.dirs.append(name)

    def test_get_tempdir_name(self):
        n = Storage('/tmp/foo/config.yaml').get_tempdir_name()
        assert n.endswith('local-compose/c07580c6520ae24a2337c9d31d96b14b')
        assert n.startswith('/')
        n2 = Storage('/tmp/foo/config.yaml').get_tempdir_name()
        assert n2.endswith('local-compose/c07580c6520ae24a2337c9d31d96b14b')
        assert n2.startswith('/')
        n2 = Storage('/tmp/foo/config.yml').get_tempdir_name()
        assert n2.endswith('local-compose/6977a6747ea71afccd5aa23a3bea7b78')
        assert n2.startswith('/')

    def test_maybe_create_tempdir(self):
        s = Storage('/tmp/foo/config.yaml')
        self.mark_dir(s.get_tempdir_name())
        s.maybe_create_tempdir()
        assert os.path.exists(s.get_tempdir_name())

    def test_clean_tempdir(self):
        s = Storage('/tmp/foo/config.yaml')
        self.mark_dir(s.get_tempdir_name())
        s.maybe_create_tempdir()
        assert os.path.exists(s.get_tempdir_name())
        s.clean_tempdir()
        assert not os.path.exists(s.get_tempdir_name())

    def test_pid_creation(self):
        s = Storage('/tmp/foo/config.yaml')
        self.mark_dir(s.get_tempdir_name())
        s.maybe_create_tempdir()
        s.pid_create()
        assert s.pid_exists()
        assert s.pid_read() > 0
