from abc import ABCMeta

from .utils import now


class Message(object):
    '''
    Represents a basic messaging entity in the system.
    '''

    __metaclass__ = ABCMeta

    def __init__(self, data, name, time=None, color=None):
        self.data = data
        self.name = name
        self.color = color
        if time is None:
            self.time = now()
        else:
            self.time = time


class Line(Message):
    '''
    Message type for Service and system information logging and output.
    '''


class Start(Message):
    '''
    Message type for Service starting.
    '''


class Stop(Message):
    '''
    Message type for Service stopping.
    '''


class Restart(Message):
    '''
    Message type for Service restarting.
    '''


class EmptyBus(Message):
    '''
    Message type that denotes empty message bus and thus finish of all components run.
    '''
