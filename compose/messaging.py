from abc import ABCMeta
try:
    import queue
except ImportError:
    import Queue as queue

from .utils import now


# Name that is used for system-wide messages output
SYSTEM_LABEL = 'system'


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


class EventBus():
    '''
    Main event messaging bus for the runtime.
    '''
    def __init__(self):
        self._bus = queue.Queue()

    def receive(self, timeout=0.1):
        '''
        Receive a message from this event bus.
        '''
        try:
            return self._bus.get(timeout=timeout)
        except queue.Empty:
            return EmptyBus(data='No messages in queue', name=SYSTEM_LABEL)

    def send(self, message):
        '''
        Send a message to this event bus.
        '''
        self._bus.put(message)

    def send_system(self, data, message_class=Line):
        '''
        Send a system-type message to this event bus.
        message_class - represents class of the message you want to send.
        '''
        self._bus.put(message_class(data=data, name=SYSTEM_LABEL))
