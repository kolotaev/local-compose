import os

import pytest
import mock

from compose.configuration import Config, ConfigurationError
from compose.service import Service
from .helpers import TMP_DIR, set_current_dir_fixture


FILE_NAME = 'unit-test-config-file.yaml'


def test_config_example():
    assert Config.example() == '''
# Specify version of the local-compose yaml schema.
version: '1'

# All global settings.
settings:
    logging:
        time-format: '%c'

# All services you want to run.
services:
    # First service with name 'web1'
    web1:
        # How to run service binary
        run: ruby server.rb
        # Directory that will be set for service run
        cwd: ~/work/microservices/billing
        # What color should service output use (console logs from service's stdout, stderr)
        color: red
        # Environment variables that are passed into service run.
        env:
            DB_USER: admin
            DB_PASS: 12345
        # Don't show service's output in console.
        silent: yes
        # Execute run service command in system shell (e.g. bash).
        shell: yes
'''


@mock.patch.object(Config, 'read')
def test_parse_with_non_existent_file(mock_read):
    conf = None
    mock_read.side_effect = IOError('File is missing in OS')
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME, '/path/workdir').parse()
    assert conf is None
    assert str(execinfo.value) == \
        'Configuration file "/path/workdir/unit-test-config-file.yaml" is invalid.\nErrors found:\nFile is missing in OS'


@mock.patch.object(Config, 'read')
def test_parse_minimal_required(mock_read):
    config_contents = '''
    version: '123.0'
    '''
    mock_read.return_value = config_contents
    conf = Config(FILE_NAME, '/path/workdir').parse()
    assert conf is not None
    assert conf.version == '123.0'
    assert conf.settings == {}
    assert conf.services == []


@mock.patch.object(Config, 'read')
def test_parse_fails_with_empty_file(mock_read):
    conf = None
    mock_read.return_value = ''
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME, '/path/workdir').parse()
    assert conf is None
    assert str(execinfo.value) == \
        'Configuration file "/path/workdir/unit-test-config-file.yaml" is invalid.\nErrors found:\nFile is empty.'


@mock.patch.object(Config, 'read')
def test_parse_fails_with_malformed_yaml_file(mock_read):
    mock_read.return_value = 'foo: {{{'
    conf = None
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME, '/path/workdir').parse()
    assert conf is None
    assert 'Configuration file "/path/workdir/unit-test-config-file.yaml" is invalid.\nErrors found:\n' in \
        str(execinfo.value)
    assert 'while parsing' in str(execinfo.value)


@mock.patch.object(Config, 'read')
def test_parse_fails_with_no_version_specified(mock_read):
    config_contents = '''
    bar: 900
    '''
    mock_read.return_value = config_contents
    conf = None
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME, '/path/workdir').parse()
    assert conf is None
    assert 'Configuration file "/path/workdir/unit-test-config-file.yaml" is invalid.\nErrors found:\n' in \
        str(execinfo.value)
    assert "'version' is a required property" in str(execinfo.value)


@mock.patch.object(Config, 'read')
def test_validate_wrong_color(mock_read):
    config_contents = '''
    version: '1.0'
    services:
        cat:
            run: cat /etc/hosts
            color: fancy-color
    '''
    mock_read.return_value = config_contents
    conf = None
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME, '/path/workdir').parse()
    assert conf is None
    assert 'Configuration file "/path/workdir/unit-test-config-file.yaml" is invalid.\nErrors found:\n' in \
        str(execinfo.value)
    assert "Color 'fancy-color' for service 'cat' is not allowed." in str(execinfo.value)


@mock.patch.object(Config, 'read')
def test_validate_wrong_color_suggestion(mock_read):
    config_contents = '''
    version: '1.0'
    services:
        cat:
            run: cat /etc/hosts
            color: grennnn
    '''
    mock_read.return_value = config_contents
    conf = None
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME, '/path/workdir').parse()
    assert conf is None
    assert 'Configuration file "/path/workdir/unit-test-config-file.yaml" is invalid.\nErrors found:\n' in \
        str(execinfo.value)
    assert "Color 'grennnn' for service 'cat' is not allowed." in str(execinfo.value)
    assert "Maybe you meant: green" in str(execinfo.value)


@mock.patch.object(Config, 'read')
def test_settings_property(mock_read):
    config_contents = '''
    version: '1.0'
    settings:
        foo: 123
        bar: asdf
    '''
    mock_read.return_value = config_contents
    conf = Config(FILE_NAME, '/path/workdir').parse()
    assert conf is not None
    assert conf.settings == {'bar': 'asdf', 'foo': 123}


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
    conf = Config(FILE_NAME, '/path/workdir').parse()
    assert len(conf.services) == 2
    assert 'web1' in list([s.name for s in conf.services])
    assert 'web2' in list([s.name for s in conf.services])
    assert isinstance(conf.services[0], Service)
    assert isinstance(conf.services[1], Service)


@mock.patch.object(Config, 'read')
@pytest.mark.parametrize('cwd_in_config, run_in_dir, expected', [
    ('cwd: /usr/bin', TMP_DIR, '/usr/bin'),
    ('cwd: /usr/bin', '/var/log', '/usr/bin'),

    ('cwd: ' + TMP_DIR, TMP_DIR, TMP_DIR),
    ('cwd: ' + TMP_DIR, '/var/log', TMP_DIR),

    ('', TMP_DIR, TMP_DIR),
    ('', '/var/log', TMP_DIR),

    ('cwd: bin', TMP_DIR, TMP_DIR + '/bin'),
    ('cwd: bin', '/usr', '/usr/bin'),

    ('cwd: ./bin', TMP_DIR, TMP_DIR + '/bin'),
    ('cwd: ./bin', '/usr', '/usr/bin'),

    ('cwd: ./bin/../', TMP_DIR, TMP_DIR),
    ('cwd: ./bin/../', '/usr', '/usr'),

    ('cwd: ~/', TMP_DIR, os.path.expanduser('~')),
    ('cwd: ~/', '/var', os.path.expanduser('~')),
])
def test_services_work_dir(mock_read, set_current_dir_fixture, cwd_in_config, run_in_dir, expected):
    assert os.getcwd() == TMP_DIR
    config = '''
    version: '1.0'
    services:
      web:
        run: ls .
        %s
    ''' % cwd_in_config
    mock_read.return_value = config
    conf = Config(filename=FILE_NAME, workdir=run_in_dir).parse()
    srv = conf.services[0]
    assert srv.cwd == expected


@mock.patch.object(Config, 'read')
def test_services_validate_cwd_inexistent(mock_read):
    config = '''
    version: '1.0'
    services:
      web:
        run: ls .
        cwd: /some/unknown/path
    '''
    mock_read.return_value = config
    with pytest.raises(ConfigurationError) as execinfo:
        conf = Config(FILE_NAME, '/path/workdir').parse()
        # conf.services
    assert str(execinfo.value) == \
        'Configuration file "/path/workdir/unit-test-config-file.yaml" is invalid.\nErrors found:\n' + \
            'Directory "/some/unknown/path" for service "web" not found'


@mock.patch.object(Config, 'read')
def test_services_validate_cwd_not_specified(mock_read):
    config = '''
    version: '1.0'
    services:
      web:
        run: ls .
    '''
    mock_read.return_value = config
    conf = Config(FILE_NAME, '/path/workdir').parse()
    assert len(conf.services) == 1


@mock.patch.object(Config, 'read')
def test_bad_env(mock_read):
    config = '''
    version: '1.0'
    services:
      web:
        run: cat /etc/hosts
        env:
          FOO:
            - the
            - array
    '''
    mock_read.return_value = config
    with pytest.raises(ConfigurationError) as execinfo:
        Config(FILE_NAME, '/path/workdir').parse()
    ex_msg = str(execinfo.value)
    assert 'Configuration file "/path/workdir/unit-test-config-file.yaml" is invalid.\nErrors found:\n' in ex_msg
    assert 'On instance' in ex_msg
    assert "['the', 'array']" in ex_msg
