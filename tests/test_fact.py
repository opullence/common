import unittest

from opulence.common.facts import BaseFact
from opulence.common.fields import BaseField, IntegerField, StringField


class TestFact(unittest.TestCase):
    def test_simple_fact(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField()

        fact = Person()
        self.assertEqual(fact.plugin_name, "superplugin")
        self.assertEqual(fact.plugin_description, "desc")
        self.assertEqual(fact.plugin_author, "nobody")
        self.assertEqual(fact.plugin_version, 42)
        self.assertFalse(fact.errored)
        self.assertEqual(fact.plugin_dependencies, ())

        self.assertTrue(fact.is_valid())
        self.assertIsInstance(fact.a, StringField, BaseField)
        self.assertIsNone(fact.a.value)
        self.assertIsNone(fact.a.default)
        self.assertFalse(fact.a.mandatory)

    def test_complex_fact(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField(value="Joe", mandatory=True)
                self.b = StringField(default="James")
                self.c = IntegerField(mandatory=True)
                self.d = IntegerField()
                self.x = "x"

        fact = Person()
        self.assertEqual(fact.plugin_name, "superplugin")
        self.assertEqual(fact.plugin_description, "desc")
        self.assertEqual(fact.plugin_author, "nobody")
        self.assertEqual(fact.plugin_version, 42)
        self.assertFalse(fact.errored)
        self.assertEqual(fact.plugin_dependencies, ())

        self.assertFalse(fact.is_valid())

        self.assertIsInstance(fact.a, StringField, BaseField)
        self.assertEqual(fact.a.value, "Joe")
        self.assertIsNone(fact.a.default)
        self.assertTrue(fact.a.mandatory)

    def test_missing_author_fact(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _version_ = 42

            def setup(self):
                self.a = StringField(value="Joe", mandatory=True)

        fact = Person()

        self.assertTrue(fact.errored)
        self.assertTrue(fact.is_valid())

    def test_missing_description_fact(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _author_ = "nobody"

        fact = Person()

        self.assertTrue(fact.errored)
        self.assertTrue(fact.is_valid())