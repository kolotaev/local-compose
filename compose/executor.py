class Executor(object):
    def __init__(self, config):
        self._conf = config
        self._services = config['services']

    def run_service(self, name):
        pass

    def run_all_services(self):
        for srv in self._services:
            self.run_service()
