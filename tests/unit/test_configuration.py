import sys

import mock
import pytest

from compose.configuration import Config


FILE_NAME = 'unit-test-config-file.yaml'


def test_config_example():
    conf = Config('/path/to/file.yaml')
    assert '' == conf.example()


@mock.patch('compose.configuration.open', create=True)
def test_parse_minimal_required(mock_open):
    config_data = '''
    version: '1.0'
    '''
    mock_open.side_effect = [
        mock.mock_open(read_data=config_data).return_value,
    ]
    conf = Config(FILE_NAME).parse()
    assert conf is not None
    assert '1.0' == conf.version


@mock.patch('compose.configuration.open', create=True)
def test_parse_fails_with_empty_file(mock_open):
    config_data = ''
    mock_open.side_effect = [
        mock.mock_open(read_data=config_data).return_value,
    ]
    conf = None
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME).parse()
    assert conf is None
    assert 'Configuration file "unit-test-config-file.yaml" is invalid.\nErrors found:\nEmpty file.' \
        in str(execinfo.value)


@mock.patch('compose.configuration.open', create=True)
def test_parse_fails_with_malformed_yaml_file(mock_open):
    config_data = 'foo: {{{'
    mock_open.side_effect = [
        mock.mock_open(read_data=config_data).return_value,
    ]
    conf = None
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME).parse()
    assert conf is None
    assert 'Configuration file "unit-test-config-file.yaml" is invalid.\nError found:\n' in str(execinfo.value)
    assert 'while parsing' in str(execinfo.value)


@mock.patch('compose.configuration.open', create=True)
def test_parse_fails_with_no_version_specified(mock_open):
    config_data = '''
    bar: 900
    '''
    mock_open.side_effect = [
        mock.mock_open(read_data=config_data).return_value,
    ]
    conf = None
    with pytest.raises(Exception) as execinfo:
        conf = Config(FILE_NAME).parse()
    assert conf is None
    assert 'Configuration file "unit-test-config-file.yaml" is invalid.\nErrors found:\n' in str(execinfo.value)
    assert "'version' is a required property" in str(execinfo.value)


@mock.patch('compose.configuration.open', create=True)
def test_settings_property(mock_open):
    config_data = '''
    version: '1.0'
    global:
        foo: 123
        bar: asdf
    '''
    mock_open.side_effect = [
        mock.mock_open(read_data=config_data).return_value,
    ]
    conf = Config(FILE_NAME).parse()
    assert conf is not None
    assert {'bar': 'asdf', 'foo': 123} == conf.settings


# @mock.patch('compose.configuration.open', create=True)
# def test_parse(mock_open):
#     config_data = '''
#     version: '1.0'
#     services:
#         web1:
#             run: ruby server-script.rb
#         web2:
#             run: java -jar /path/to/server.jar
#     '''
#     mock_open.side_effect = [
#         mock.mock_open(read_data=config_data).return_value,
#     ]
#     conf = Config('unit-test-config-file.yaml').parse()
#     assert conf is not None
#     assert '1.0' == conf.version
#     assert {'foo': 123} == conf.settings
#     assert 2 == len(conf.services)
