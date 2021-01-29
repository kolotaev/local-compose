class Readiness(object):
    '''
    Class is responsible for determining whether service/job is running, needs restart, state of comletion, etc.
    '''
    def __init__(self, readiness_config):
        self.srv_rc = None
        if readiness_config is None:
            readiness_config = {}
        self.expected_to_retry = 'retry' in readiness_config
        retry_conf = readiness_config.get('retry', {})
        self.retry = RetryLogic(retry_conf.get('attempts'), retry_conf.get('wait'))

    def update_service_state(self, returncode):
        '''
        Update service execution state.
        '''
        self.srv_rc = returncode

    def needs_retry(self):
        '''
        Do we need to retry?
        '''
        if not self.expected_to_retry:
            return False, 0
        is_failed = self.srv_rc is not None and self.srv_rc != 0
        needs = is_failed and not self.retry.finished
        return (needs, self.retry.wait)


class RetryLogic(object):
    '''
    Class that is responsible for service/job restarts related actions.
    attempts: How many times to try? Default: infinite
    wait: How many seconds to wait between attempts? Default: 5 seconds.
    '''
    def __init__(self, attempts=None, wait=None):
        self._done_attempts = 0
        if attempts is None:
            attempts = float('inf')
        self.attempts = attempts
        if wait is None:
            wait = 5
        self.wait = wait

    @property
    def finished(self):
        '''
        Did we exceeded attempts and thus finished retrying?
        '''
        if self._done_attempts < self.attempts:
            self._done_attempts += 1
            return False
        return True
