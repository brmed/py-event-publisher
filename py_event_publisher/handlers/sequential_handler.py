# coding:utf-8
from .base_handler import BaseHandler


class SequentialHandler(BaseHandler):

    def __init__(self, watchers):
        self.__watchers = list(watchers)

    def __call__(self, *args, **kwargs):
        passing_arg = self.notify(*args, **kwargs)
        for watcher in self.__watchers:
            passing_arg = watcher(**passing_arg)
