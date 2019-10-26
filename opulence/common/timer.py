from datetime import datetime


class Clock:
    def __init__(self):
        self.start_date = None
        self.end_date = None

    def start(self):
        self.end_date = None
        self.start_date = datetime.now()

    def stop(self):
        self.end_date = datetime.now()

    @property
    def time_elapsed(self):
        assert self.start_date, "Can't check 'time_elapsed' on an unstarted Clock"
        if self.end_date:
            return self.end_date - self.start_date
        return datetime.now() - self.start_date
