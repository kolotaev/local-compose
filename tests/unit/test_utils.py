from compose.utils import now


def test_now():
    one = now()
    two = now()
    assert two > one
