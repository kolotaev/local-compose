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
        web2:
            run: java -jar /path/to/server.jar
            color: red
            cwd: this-dir
            env:
                FOO: 123
            silent: yes
            shell: no
    '''
    mock_read.return_value = config_contents
    conf = Config(FILE_NAME).parse()
    assert 1 == len(conf.services)
    assert 'web2' == conf.services[0].name
    assert 'java -jar /path/to/server.jar' == conf.services[0].cmd
    assert 'red' == conf.services[0].color
    assert 'this-dir' == conf.services[0].cwd
    assert {'FOO': 123} == conf.services[0].env
    assert conf.services[0].quiet
    assert not conf.services[0].in_shell
