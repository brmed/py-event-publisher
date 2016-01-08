# coding:utf-8
from collections import defaultdict
from notify.all import Signal as PyNotifySignal
from notify.all import AbstractSignal

from py_event_publisher.handlers import BaseHandler


class Signal(PyNotifySignal):

    def get_exception_handler(self):
        return AbstractSignal.reraising_exception_handler


class UnsubscribedEventException(Exception):
    """
    Exception to be raised if event wasn't subscribed.
    """


class ObserverWithoutPublishException(Exception):
    """
    Exception to be raised if observer does not implements publish interface.
    """


class EventPublisher(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            instance = super(EventPublisher, cls).__new__(cls, *args, **kwargs)
            instance.observers = {}
            instance.__connected_classes = defaultdict(list)
            cls._instance = instance
        return cls._instance

    def __already_subscribed(self, event_key, observer):
        return str(observer.__class__) in self.__connected_classes[event_key]

    def __is_valid_observer(self, observer):
        return issubclass(observer.__class__, BaseHandler)

    def __connect(self, event_key, observer):
        self.observers[event_key].connect(observer)
        self.__connected_classes[event_key].append(str(observer.__class__))

    def subscribe(self, event_key, observer):
        if not self.__is_valid_observer(observer):
            raise ObserverWithoutPublishException(u"Observer: {}".format(observer))

        if self.__already_subscribed(event_key, observer):
            return

        if event_key not in self.observers:
            self.observers[event_key] = Signal()
        self.__connect(event_key, observer)

    def publish(self, event_key, **kwargs):
        if event_key not in self.observers:
            raise UnsubscribedEventException(u"Event name: {}".format(event_key))

        signal = self.observers[event_key]
        signal(**kwargs)

    def reset(self):
        self.observers = {}
        self.__connected_classes = defaultdict(list)
