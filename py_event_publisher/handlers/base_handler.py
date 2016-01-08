# coding:utf-8
from abc import ABCMeta, abstractmethod


class BaseHandler(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        self.notify(*args, **kwargs)
