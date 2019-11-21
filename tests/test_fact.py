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

    def test_valid_fact_0(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField(mandatory=True)
                self.b = StringField()

        fact = Person(a="yes")
        self.assertTrue(fact.is_valid())

    def test_valid_fact_1(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField(mandatory=True, default="aze")
                self.b = StringField()

        fact = Person(a="yes")
        self.assertTrue(fact.is_valid())

    def test_invalid_fact_0(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField(mandatory=True, default="def")
                self.b = StringField()

        fact = Person()
        self.assertFalse(fact.is_valid())

    def test_invalid_fact__1(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _description_ = "desc"
            _author_ = "nobody"
            _version_ = 42

            def setup(self):
                self.a = StringField(mandatory=True, default="def")
                self.b = StringField()

        fact = Person(a="def")
        self.assertFalse(fact.is_valid())

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

    def test_facts_hash(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _author_ = "nobody"
            _description_ = "desc"

            def setup(self):
                self.a = StringField()

        a = Person()
        b = Person()
        c = Person()
        self.assertEqual(hash(a), hash(b), hash(c))

    def test_facts_hash_invalid_plugin(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _description_ = "desc"

            def setup(self):
                self.a = StringField()

        a = Person()
        b = Person()
        c = Person()
        self.assertEqual(hash(a), hash(b), hash(c))

    def test_empty_facts_hash_comparison(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _description_ = "desc"

        a = Person()
        aa = Person()
        b = Person(a="joe")
        c = Person(a="joe")
        self.assertNotEqual(hash(a), hash(b))
        self.assertNotEqual(hash(a), hash(aa))
        self.assertNotEqual(hash(b), hash(c))

        self.assertEqual(a.plugin_category, "BaseFact")

    def test_facts_hash_comparison(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _description_ = "desc"

            def setup(self):
                self.a = StringField()

        a = Person(a="joe")
        b = Person(a="joe")
        c = Person(a="job")
        self.assertEqual(hash(a), hash(b))
        self.assertNotEqual(hash(a), hash(c))
        self.assertNotEqual(hash(b), hash(c))

    def test_complex_facts_hash_comparison(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _description_ = "desc"

            def setup(self):
                self.a = StringField(default="42")
                self.b = IntegerField(default=42)
                self.c = IntegerField(default=424242)

        a = Person(a="42", b=42, c=424242)
        b = Person(a=42, b="42")
        c = Person(a="42", b=42, c=424242)
        d = Person()
        e = Person(a="42", b=43, c=424242)
        self.assertEqual(hash(a), hash(b), hash(c))
        self.assertEqual(hash(b), hash(c), hash(d))
        self.assertNotEqual(hash(e), hash(a))
        self.assertNotEqual(hash(e), hash(b))
        self.assertNotEqual(hash(e), hash(c))
        self.assertNotEqual(hash(e), hash(d))

    def test_get_info(self):
        class Person(BaseFact):
            _name_ = "superplugin"
            _version_ = 42
            _description_ = "desc"

            def setup(self):
                self.a = StringField(default="42")
                self.b = IntegerField()
                self.c = IntegerField(default=424242)

        a = Person(a="42", c=424242)

        infos = a.get_info()
        self.assertTrue("plugin_data" in infos)
        self.assertTrue(
            {"name": "a", "mandatory": False, "value": "42"} in infos["fields"]
        )
        self.assertTrue(
            {"name": "b", "mandatory": False, "value": None} in infos["fields"]
        )
