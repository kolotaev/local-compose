from compose.info import version, name


def test_version():
    assert '0.3.0' == version


def test_name():
    assert 'local-compose' == name
