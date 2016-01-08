# coding:utf-8
import pytest
from unittest import TestCase

from py_event_publisher.handlers import BaseHandler, SequentialHandler


class MockedSequentialHandler(SequentialHandler):

    def __init__(self, *args, **kwargs):
        super(MockedSequentialHandler, self).__init__(*args, **kwargs)
        self.notify_called = False

    def notify(self, *args, **kwargs):
        self.notify_called = True
        return {'returned_arg': 'value'}


class MockedSequentialWatcher(BaseHandler):

    def __init__(self):
        self.notify_called = False
        self.passed_arg = None

    def notify(self, **passed_arg):
        self.notify_called = True
        self.passed_arg = passed_arg
        return self.passed_arg


class SequentialHandlerTests(TestCase):

    def test_call_magic_method_calls_notify(self):
        watcher = MockedSequentialWatcher()
        handler = MockedSequentialHandler([watcher])

        assert handler.notify_called is False
        assert watcher.notify_called is False

        handler()

        assert handler.notify_called is True
        assert watcher.notify_called is True
        assert {'returned_arg': 'value'} == watcher.passed_arg

    def test_handler_is_abstract_class(self):
        with pytest.raises(TypeError):
            SequentialHandler()
