import os

import pytest

from compose.service import Service, Job
from .helpers import TMP_DIR, set_current_dir_fixture


def test_service_type():
    s = Service('my-srv', 'while true; do echo "hello"; done')
    assert isinstance(s, Service)
    j = Job('my-job', 'cat /etc/hosts')
    assert isinstance(j, Job)


@pytest.mark.parametrize('type_class, cmd', [
    (Job, 'cat /etc/hosts'),
    (Service, 'while true; do echo "hello"; done'),
])
def test_service_default_properties(set_current_dir_fixture, type_class, cmd):
    s = type_class('test-srv', cmd)
    assert s.name == 'test-srv'
    assert s.cmd == cmd
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
    assert s.name == 'test-srv'
    assert s.cmd == cmd
    assert s.quiet
    assert s.color == 'red'
    assert s.env == {'FOO': '1'}
    assert s.cwd == '/home'
    assert not s.in_shell
