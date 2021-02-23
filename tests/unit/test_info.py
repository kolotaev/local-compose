from compose.info import VERSION, NAME


def test_version():
    assert VERSION == '0.4.0'


def test_name():
    assert NAME == 'local-compose'
