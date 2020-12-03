import mock
import pytest

from compose.configuration import Config
from compose.service import Service


FILE_NAME = 'unit-test-config-file.yaml'


def test_config_example():
    assert Config.example() == '''
# Specify version of the local-compose yaml schema.
version: '1'

# All global settings.
global:
    foo: 123

# All services you want to run.
services:
    # First service with name 'web1'
    web1:
        # How to run service binary
        run: ruby server.rb
        # Directory that will be set for service run
        cwd: /home/me/work/microservices/billing
        # What color should service output use (console logs from service's stdout, stderr)
        color: red
        # Environment variables that are passed into service run.
        env:
            DB_USER: admin
            DB_PASS: 12345
        # Show service's output in console.
        silent: yes
        # Don't execute run service command in system shell (e.g. bash).
        shell: no
'''


@mock.patch.object(Config, 'read')
def test_parse_with_non_existent_file(mock_read):
    conf = None
    mock_read.side_effect = IOError('File is missing in OS')
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME).parse()
    assert conf is None
    assert 'Configuration file "unit-test-config-file.yaml" is invalid.\nErrors found:\nFile is missing in OS' \
        == str(execinfo.value)


@mock.patch.object(Config, 'read')
def test_parse_minimal_required(mock_read):
    config_contents = '''
    version: '123.0'
    '''
    mock_read.return_value = config_contents
    conf = Config(FILE_NAME).parse()
    assert conf is not None
    assert '123.0' == conf.version
    assert {} == conf.settings
    assert [] == conf.services


@mock.patch.object(Config, 'read')
def test_parse_fails_with_empty_file(mock_read):
    conf = None
    mock_read.return_value = ''
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME).parse()
    assert conf is None
    assert 'Configuration file "unit-test-config-file.yaml" is invalid.\nErrors found:\nFile is empty.' \
        == str(execinfo.value)


@mock.patch.object(Config, 'read')
def test_parse_fails_with_malformed_yaml_file(mock_read):
    mock_read.return_value = 'foo: {{{'
    conf = None
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME).parse()
    assert conf is None
    assert 'Configuration file "unit-test-config-file.yaml" is invalid.\nErrors found:\n' in str(execinfo.value)
    assert 'while parsing' in str(execinfo.value)


@mock.patch.object(Config, 'read')
def test_parse_fails_with_no_version_specified(mock_read):
    config_contents = '''
    bar: 900
    '''
    mock_read.return_value = config_contents
    conf = None
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME).parse()
    assert conf is None
    assert 'Configuration file "unit-test-config-file.yaml" is invalid.\nErrors found:\n' in str(execinfo.value)
    assert "'version' is a required property" in str(execinfo.value)


@mock.patch.object(Config, 'read')
def test_settings_property(mock_read):
    config_contents = '''
    version: '1.0'
    global:
        foo: 123
        bar: asdf
    '''
    mock_read.return_value = config_contents
    conf = Config(FILE_NAME).parse()
    assert conf is not None
    assert {'bar': 'asdf', 'foo': 123} == conf.settings


@mock.patch.object(Config, 'read')
def test_services_property(mock_read):
    config_contents = '''
    version: '1.0'
    services:
        web1:
            run: ruby server-script.rb
        web2:
            run: java -jar /path/to/server.jar
    '''
    mock_read.return_value = config_contents
    conf = Config(FILE_NAME).parse()
    assert 2 == len(conf.services)
    assert 'web1' in list([s.name for s in conf.services])
    assert 'web2' in list([s.name for s in conf.services])
    assert isinstance(conf.services[0], Service)
    assert isinstance(conf.services[1], Service)
