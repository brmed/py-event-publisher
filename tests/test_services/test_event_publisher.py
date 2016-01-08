# coding:utf-8
import pytest
from mock import Mock, patch
from unittest import TestCase

from py_event_publisher.handlers import BaseHandler
from py_event_publisher.services import EventPublisher, UnsubscribedEventException, ObserverWithoutPublishException


class Handler(BaseHandler):

    def notify(self, *args, **kwargs):
        pass


class ExceptionHandler(BaseHandler):

    def notify(self, *args, **kwargs):
        raise NotImplementedError


class EventPublisherTests(TestCase):

    def setUp(self):
        self.observer = Handler()
        self.events_publisher = EventPublisher()
        self.patcher = patch('py_event_publisher.services.event_publisher.Signal')
        self.MockedSignal = self.patcher.start()

    def tearDown(self):
        self.events_publisher.reset()
        self.patcher.stop()

    def test_events_publisher_initialization(self):
        assert self.events_publisher.observers == {}

    def test_reset_observers(self):
        self.events_publisher.subscribe('event_key', self.observer)
        assert self.events_publisher.observers != {}
        self.events_publisher.reset()
        assert self.events_publisher.observers == {}

    def test_should_register_observer_to_event(self):
        self.events_publisher.subscribe('event_key', self.observer)

        signal_instance = self.MockedSignal()
        assert self.events_publisher.observers == {'event_key': signal_instance}

        signal_instance.connect.assert_called_once_with(self.observer)

    def test_should_publish_all_events(self):
        signal_instance = self.MockedSignal()
        self.events_publisher.subscribe('event_key', self.observer)

        kwargs = {'arg1': 'value1', 'arg2': 'value2'}
        self.events_publisher.publish('event_key', **kwargs)

        signal_instance.assert_called_once_with(**kwargs)

    def test_can_not_connect_listener_from_same_class_twice(self):
        self.events_publisher.subscribe('event_key', self.observer)
        self.events_publisher.subscribe('event_key', Handler())

        signal_instance = self.MockedSignal()
        signal_instance.connect.assert_called_once_with(self.observer)

    def test_raises_custom_exception_if_tries_to_publish_unsubscribed_event(self):
        with pytest.raises(UnsubscribedEventException):
            self.events_publisher.publish('unsubscribed_event')

    def test_raises_custom_exception_if_tries_to_subscribe_event_wich_not_subclass_event_handler(self):
        class Foo():

            def publish(self, *args, **kwargs):
                pass

        with pytest.raises(ObserverWithoutPublishException):
            self.events_publisher.subscribe('event_key', Foo())

    def test_raises_custom_exception_if_tries_to_subscribe_event_with_non_callable_publish(self):
        observer = Mock(publish=10)
        with pytest.raises(ObserverWithoutPublishException):
            self.events_publisher.subscribe('event_key', observer)

    def test_singleton(self):
        publisher = EventPublisher()
        self.events_publisher.subscribe('event_key', self.observer)
        signal_instance = self.MockedSignal()

        assert self.events_publisher.observers == {'event_key': signal_instance}
        assert publisher.observers == {'event_key': signal_instance}
        assert id(self.events_publisher) == id(publisher)
        assert id(self.events_publisher.observers) == id(publisher.observers)

    def test_updates_connected_classes_for_multiple_objects(self):
        class Foo(BaseHandler):

            def notify(self, *args, **kwargs):
                pass

        self.events_publisher.subscribe('event_key', self.observer)
        self.events_publisher.subscribe('event_key', Foo())

        observers = self.events_publisher._EventPublisher__connected_classes

        assert str(self.observer.__class__) in observers['event_key']
        assert str(Foo().__class__) in observers['event_key']

class TestEventsPublisherNonMocked(TestCase):

    def setUp(self):
        self.events_publisher = EventPublisher()

    def test_raises_exception(self):
        observer = ExceptionHandler()

        self.events_publisher.subscribe('event_key', observer)
        with pytest.raises(NotImplementedError):
            self.events_publisher.publish('event_key')
