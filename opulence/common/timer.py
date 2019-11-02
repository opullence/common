from .patterns import JsonSerializable
from .utils import now


class Clock(JsonSerializable):
    def __init__(self, start_date=None, end_date=None, started=False):
        self.start_date = start_date
        self.end_date = end_date
        self.started = started

    def start(self):
        self.started = True
        self.end_date = None
        self.start_date = now()

    def stop(self):
        self.started = False
        self.end_date = now()

    @property
    def time_elapsed(self):
        assert self.start_date, "Can't check 'time_elapsed' on an unstarted Clock"
        if self.end_date:
            return self.end_date - self.start_date
        return now() - self.start_date
