import unittest

from opulence.common.bases.baseFact import BaseFact
from opulence.common.fields import IntegerField, StringField


class A(BaseFact):
    _name_ = "xx"
    _description_ = "xx"
    _author_ = "xx"
    _version_ = 1

    def setup(self):
        self.a = IntegerField()
        self.b = StringField(default="b")
        self.c = StringField(default="c")


class B(BaseFact):
    _name_ = "xx"
    _description_ = "xx"
    _author_ = "xx"
    _version_ = 1

    def setup(self):
        self.a = IntegerField()
        self.b = StringField(default="b")
        self.c = StringField(default="c")


class TestFactComparison(unittest.TestCase):
    def test_fact_equal(self):
        fact_a = A(a=42, b="bb", c="cc")
        fact_aa = A(a=42, b="bb", c="cc")

        self.assertEqual(fact_a, fact_aa)

    def test_fact_not_equal(self):
        fact_a = A(a=42, b="bb", c="cc")
        fact_aa = A(a=24, b="bb", c="cc")

        self.assertNotEqual(fact_a, fact_aa)

    def test_fact_not_equal(self):
        fact_a = A(a=42, b="bb", c="cc")
        fact_b = B(a=42, b="bb", c="cc")

        self.assertNotEqual(fact_a, fact_b)
