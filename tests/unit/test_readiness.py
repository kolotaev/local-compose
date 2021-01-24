import pytest

from compose.readiness import Readiness, RetryLogic


@pytest.mark.parametrize('config', [
    ({}),
    ({
        'retry': {}
    }),
])
def test_readiness_empty_config_create_defaults(config):
    r = Readiness(config)
    assert r.retry is not None
    assert r.retry.attempts == float('inf')
    assert r.retry.wait == 5


def test_readiness():
    conf = {
        'retry': {
            'wait': 30,
            'attempts': 50,
        },
    }
    r = Readiness(conf)
    assert r.retry is not None
    assert r.retry.attempts == 50
    assert r.retry.wait == 30


def test_retry_logic_defaults():
    r = RetryLogic()
    assert r.attempts == float('inf')
    assert r.wait == 5


def test_retry_logic_needs_retry():
    r = RetryLogic(2, 5)
    assert r.needs_retry()
    assert r.needs_retry()
    assert not r.needs_retry()
    assert not r.needs_retry()
