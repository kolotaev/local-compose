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

def test_readiness_needs_retry_no_retry_config():
    r = Readiness({})
    assert r.needs_retry() == (False, 0)


def test_readiness_needs_retry_only_retries_exceed():
    r = Readiness({
        'retry': {
            'attempts': 3,
            'wait': 7,
        },
    })
    assert r.needs_retry() == (False, 7)
    r.update_service_state(-1)
    assert r.needs_retry() == (True, 7)
    r.retry.do_retry()
    assert r.needs_retry() == (True, 7)
    r.retry.do_retry()
    assert r.needs_retry() == (True, 7)
    r.retry.do_retry()
    assert r.needs_retry() == (False, 7)


def test_readiness_needs_retry_with_update_state_interlude():
    r = Readiness({
        'retry': {
            'attempts': 3,
            'wait': 7,
        },
    })
    assert r.needs_retry() == (False, 7)
    r.update_service_state(-1)
    assert r.needs_retry() == (True, 7)
    r.retry.do_retry()
    assert r.needs_retry() == (True, 7)
    r.update_service_state(0)
    assert r.needs_retry() == (False, 7)
    r.update_service_state(-9)
    assert r.needs_retry() == (True, 7)
    r.retry.do_retry()
    assert r.needs_retry() == (True, 7)
    r.update_service_state(None)
    assert r.needs_retry() == (False, 7)
    r.update_service_state(-3)
    assert r.needs_retry() == (True, 7)
    r.update_service_state(-40)
    r.update_service_state(-50)
    assert r.needs_retry() == (True, 7)
    r.retry.do_retry()
    assert r.needs_retry() == (False, 7)


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


def test_retry_logic_finished():
    r = RetryLogic(attempts=2)
    assert not r.finished
    assert not r.finished
    r.do_retry()
    assert not r.finished
    r.do_retry()
    assert r.finished
    assert r.finished
