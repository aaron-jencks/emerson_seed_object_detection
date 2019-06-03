import multiprocessing as mp
from multiprocessing.managers import BaseManager
from collections import deque
import os


class DequeManager(BaseManager):
    pass


class DequeProxy(object):
    def __init__(self, *args):
        self.deque = deque(*args)

    def __str__(self):
        return str(self.deque)

    def __contains__(self, item):
        return item in self.deque

    def __len__(self):
        return self.deque.__len__()

    def appendleft(self, x):
        self.deque.appendleft(x)

    def append(self, x):
        self.deque.append(x)

    def pop(self):
        return self.deque.pop()

    def popleft(self):
        return self.deque.popleft()


class DictProxy(object):
    def __init__(self, *args):
        self.d = dict(*args)

    def __getitem__(self, item):
        if item in self.d:
            return self.d[item]

    def __setitem__(self, key, value):
        self.d[key] = value

    def __str__(self):
        return str(self.d)

    def __contains__(self, item):
        return item in self.d

    def __len__(self):
        return len(self.d)

    def keys(self):
        return self.d.keys()

    def values(self):
        return self.d.values()


DequeManager.register('DequeProxy', DequeProxy,
                      exposed=['__str__', '__contains__', '__len__', 'append', 'appendleft',
                               'pop', 'popleft'])

DequeManager.register('DictProxy', DictProxy,
                      exposed=['__str__', '__contains__', '__getitem__', '__setitem__', '__len__', 'keys', 'values'])


class Op:
    """A wrapper class for passing data to the MPProcessor class via a deque
    When the data is recieved, the op is applied to every value of data.
    Once the data is processed, then callback is called with the finished data"""

    def __init__(self, data: iter, op: callable, callback: callable):
        self.data = data
        self.op = op
        self.callback = callback


class MPProcessor:
    def __init__(self):
        self.pool = mp.Pool(os.cpu_count())

    def execute(self, data: iter, op: callable):
        return self.pool.map(op, data)
