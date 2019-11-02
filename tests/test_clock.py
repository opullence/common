import unittest

from opulence.common.timer import Clock


class TestStringField(unittest.TestCase):
    def test_estarted_clock(self):
        c = Clock()
        self.assertFalse(c.started)
        c.start()
        self.assertTrue(c.started)
