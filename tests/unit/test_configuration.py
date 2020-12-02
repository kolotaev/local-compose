import mock
import pytest

from compose.configuration import Config


FILE_NAME = 'unit-test-config-file.yaml'


def test_config_example():
    conf = Config('/path/to/file.yaml')
    assert '' == conf.example()


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


# # @mock.patch('compose.configuration.open', create=True)
# # def test_parse(mock_open):
# #     config_contents = '''
# #     version: '1.0'
# #     services:
# #         web1:
# #             run: ruby server-script.rb
# #         web2:
# #             run: java -jar /path/to/server.jar
# #     '''
# #     mock_open.side_effect = [
# #         mock.mock_open(read_data=config_contents).return_value,
# #     ]
# #     conf = Config('unit-test-config-file.yaml').parse()
# #     assert conf is not None
# #     assert '1.0' == conf.version
# #     assert {'foo': 123} == conf.settings
# #     assert 2 == len(conf.services)
