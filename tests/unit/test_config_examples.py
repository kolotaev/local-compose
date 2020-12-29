import mock
import pytest

from compose.configuration import Config
from compose.service import Service


FILE_NAME = 'unit-test-config-file.yaml'


@mock.patch.object(Config, 'read')
def test_services_all_items_are_passed(mock_read):
    config_contents = '''
    version: '1.0'
    services:
        web1:
            run: java -jar /path/to/server.jar
            color: red
            cwd: /path/to/your/dir
            env:
                FOO: 123
                BAR: asdf
            silent: yes
            shell: no
    '''
    mock_read.return_value = config_contents
    conf = Config(FILE_NAME).parse()
    assert 1 == len(conf.services)
    web1 = conf.services[0]
    assert 'web1' == web1.name
    assert 'java -jar /path/to/server.jar' == web1.cmd
    assert 'red' == web1.color
    assert '/path/to/your/dir' == web1.cwd
    assert 'FOO' in web1.env
    assert 123 == web1.env['FOO']
    assert 'BAR' in web1.env
    assert 'asdf' == web1.env['BAR']
    assert web1.quiet
    assert not web1.in_shell


@pytest.mark.skip
@mock.patch.object(Config, 'read')
def test_ready_probe(mock_read):
    config_contents = '''
    version: '1.0'
    services:
        web1:
            run: java -jar /path/to/server.jar
            readyProbe:
                tcpCheck:
                    endpoint: aakshskahk
                httpCheck:
                    url: aakshskahk
                retry:
                    attempts: 12
    '''
    mock_read.return_value = config_contents
    conf = Config(FILE_NAME).parse()
    assert 1 == len(conf.services)
