import pytest
import mock

from compose.configuration import Config


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
    assert len(conf.services) == 1
    web1 = conf.services[0]
    assert web1.name == 'web1'
    assert web1.cmd == 'java -jar /path/to/server.jar'
    assert web1.color == 'red'
    assert web1.cwd == '/path/to/your/dir'
    assert 'FOO' in web1.env
    # check that everything is converted into string for valid shell ENV
    assert web1.env['FOO'] == '123'
    assert 'BAR' in web1.env
    assert web1.env['BAR'] == 'asdf'
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
    assert len(conf.services) == 1
