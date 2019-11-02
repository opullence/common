from datetime import datetime

from .patterns import JsonSerializable


class Clock(JsonSerializable):
    def __init__(self, start_date=None, end_date=None, started=False):
        self.start_date = start_date
        self.end_date = end_date
        self.started = started

    def start(self):
        self.end_date = None
        self.started = True
        self.start_date = datetime.now()

    def stop(self):
        self.started = False
        self.end_date = datetime.now()

    @property
    def time_elapsed(self):
        assert self.start_date, "Can't check 'time_elapsed' on an unstarted Clock"
        if self.end_date:
            return self.end_date - self.start_date
        return datetime.now() - self.start_date
