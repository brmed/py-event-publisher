# coding:utf-8
import pytest
from unittest import TestCase

from py_event_publisher.handlers import BaseHandler


class BaseHandlerTests(TestCase):

    class MockedHandler(BaseHandler):

        def __init__(self):
            self.notify_called = False

        def notify(self, *args, **kwargs):
            self.notify_called = True

    def test_call_magic_method_calls_notify(self):
        handler = self.MockedHandler()
        self.assertFalse(handler.notify_called)

        handler()

        assert handler.notify_called is True

    def test_base_handler_is_abstract_class(self):
        with pytest.raises(TypeError):
            BaseHandler()
