import os

import pytest

from compose.service import Service, Job


TMP_DIR = os.path.join(os.path.dirname(__file__), 'local-compose-tmp-dir-test')


@pytest.fixture
def set_current_dir():
    real_cwd = os.getcwd()
    os.makedirs(TMP_DIR)
    os.chdir(TMP_DIR)
    yield
    os.rmdir(TMP_DIR)
    os.chdir(real_cwd)


def test_service_type():
    s = Service('my-srv', 'while true; do echo "hello"; done')
    assert isinstance(s, Service)
    j = Job('my-job', 'cat /etc/hosts')
    assert isinstance(j, Job)


@pytest.mark.parametrize('type_class, cmd', [
    (Job, 'cat /etc/hosts'),
    (Service, 'while true; do echo "hello"; done'),
])
def test_service_default_properties(set_current_dir, type_class, cmd):
    s = type_class('test-srv', cmd)
    assert 'test-srv' == s.name
    assert cmd == s.cmd
    assert not s.quiet
    assert s.color is None
    assert s.env is None
    assert s.cwd == TMP_DIR
    assert not s.in_shell


@pytest.mark.parametrize('type_class, cmd', [
    (Job, 'cat /etc/hosts'),
    (Service, 'while true; do echo "hello"; done'),
])
def test_service_properties(type_class, cmd):
    s = type_class('test-srv', cmd, color='red', env={'FOO': '1'}, cwd='/home', shell=False, quiet=True)
    assert 'test-srv' == s.name
    assert cmd == s.cmd
    assert s.quiet
    assert 'red' == s.color
    assert {'FOO': '1'} == s.env
    assert '/home' == s.cwd
    assert not s.in_shell


@pytest.mark.parametrize('cwd, expected', [
    ('/usr/bar/baz', '/usr/bar/baz'),
    (TMP_DIR, TMP_DIR),
    (None, TMP_DIR),
    ('my/dir', TMP_DIR + '/my/dir'),
    ('./bar/baz', TMP_DIR + '/bar/baz'),
    ('./bar/../', TMP_DIR),
    # ('~/my/dir', '/tmp/foo/bar/my/dir'),
])
def test_work_dir(set_current_dir, cwd, expected):
    s = Service('web1', 'echo 123', cwd=cwd)
    assert expected == s.cwd
