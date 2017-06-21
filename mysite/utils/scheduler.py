# coding=utf-8
# multi threading scheduler task
from threading import Timer


class MultiThreadScheduler(object):
    def __init__(self, sleep_time, func):
        self.sleep_time = sleep_time
        self.function = func
        self._t = None

    def start(self):
        if self._t is None:
            self._t = Timer(self.sleep_time, self._run)
            self._t.start()
        else:
            raise Exception("this timer is already running")

    def _run(self):
        self.function()
        self._t = Timer(self.sleep_time, self._run)
        self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None
