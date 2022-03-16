import mock

from compose.configuration import Config


FILE_NAME = 'unit-test-config-file.yaml'


@mock.patch.object(Config, 'read')
def test_default_values_from_schema_in_settings(mock_read):
    config_contents = '''
    version: '1'
    '''
    mock_read.return_value = config_contents
    conf = Config(FILE_NAME, '/path/to/workdir').parse()
    assert conf.settings == {
        'logging': {
            'timeFormat': '%H:%M:%S',
            'usePrefix': True,
            'toStdout': True,
            'toFile': {
                'enabled': False,
                'maxSize': 0,
                'count': 0,
            },
        },
    }
