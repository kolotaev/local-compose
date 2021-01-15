from compose.info import VERSION, NAME


def test_version():
    assert '0.3.0' == VERSION


def test_name():
    assert 'local-compose' == NAME
