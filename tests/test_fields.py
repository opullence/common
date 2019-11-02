import unittest

from opulence.common.fields import IntegerField, StringField


class TestStringField(unittest.TestCase):
    def test_empty_stringfield(self):
        s = StringField()
        self.assertEqual(s.value, None)
        self.assertEqual(s.mandatory, False)
        self.assertEqual(s.default, None)

    def test_simple_stringfield(self):
        s = StringField("foo")
        self.assertEqual(s.value, "foo")
        self.assertEqual(s.mandatory, False)
        self.assertEqual(s.default, None)

    def test_full_stringfield(self):
        s = StringField("foo", mandatory=True, default="Bar")
        self.assertEqual(s.value, "foo")
        self.assertEqual(s.mandatory, True)
        self.assertEqual(s.default, "Bar")

    def test_cast_stringfield(self):
        s = StringField(value=123, mandatory=True, default=12345)
        self.assertEqual(s.value, "123")
        self.assertEqual(s.mandatory, True)
        self.assertEqual(s.default, "12345")


class TestIntegerField(unittest.TestCase):
    def test_empty_integerfield(self):
        s = IntegerField()
        self.assertEqual(s.value, None)
        self.assertEqual(s.mandatory, False)
        self.assertEqual(s.default, None)

    def test_simple_integerfield(self):
        s = IntegerField(42)
        self.assertEqual(s.value, 42)
        self.assertEqual(s.mandatory, False)
        self.assertEqual(s.default, None)

    def test_full_integerfield(self):
        s = IntegerField(42, mandatory=True, default=4242)
        self.assertEqual(s.value, 42)
        self.assertEqual(s.mandatory, True)
        self.assertEqual(s.default, 4242)

    def test_cast_integerfield(self):
        s = IntegerField(value="42", mandatory=True, default="4242")
        self.assertEqual(s.value, 42)
        self.assertEqual(s.mandatory, True)
        self.assertEqual(s.default, 4242)

    # def test_impossible_cast_integerfield(self):
    #     s = IntegerField(value="john", mandatory=True, default="snow")
    #     self.assertEqual(s.value, 42)
    #     self.assertEqual(s.mandatory, True)
    #     self.assertEqual(s.default, 4242)
