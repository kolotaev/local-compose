import pytest

from compose.service import Service, Job


def test_service_type():
    s = Service('my-srv', 'while true; do echo "hello"; done')
    assert isinstance(s, Service)
    j = Job('my-job', 'cat /etc/hosts')
    assert isinstance(j, Job)


@pytest.mark.parametrize('type_class, cmd', [
    (Job, 'cat /etc/hosts'),
    (Service, 'while true; do echo "hello"; done'),
])
def test_service_default_properties(type_class, cmd):
    s = type_class('test-srv', cmd)
    assert 'test-srv' == s.name
    assert cmd == s.cmd
    assert not s.quiet
    assert s.color is None
    assert s.env is None
    assert s.cwd is None
    assert s.in_shell


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

