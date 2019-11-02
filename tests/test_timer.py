import unittest

from opulence.common.timer import Clock


class TestClock(unittest.TestCase):
    def test_clock_starting(self):
        c = Clock()
        c.start()
        self.assertTrue(c.started)
