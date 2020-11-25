class Service(object):
    def __init__(self, cmd, name=None, color=None, quiet=False, env=None, cwd=None, shell=True):
        self.cmd = cmd
        self.color = color
        self.quiet = quiet
        self.name = name
        self.env = env
        self.cwd = cwd
        self.in_shell = shell

class Job(Service):
    pass
