import unittest
import json

from opulence.common.jsonEncoder import encode, decode
from opulence.common.bases.baseFact import BaseFact
from opulence.common.fields import StringField, IntegerField
from opulence.common.job import Composable, Result

class TestJsonEncodeStringField(unittest.TestCase):
    def test_encode_stringfield(self):
        s = StringField(value="Foo", default="Bar", mandatory=True)
        s_json = json.dumps(s, cls=encode)
        new_s = json.loads(s_json, object_hook=decode)

        self.assertIsInstance(new_s.value, str)
        self.assertIsInstance(new_s.default, str)

        self.assertEqual(new_s.value, s.value)
        self.assertEqual(new_s.default, s.default)
        self.assertEqual(new_s.mandatory, s.mandatory)

    def test_encode_cast_stringfield(self):
        s = StringField(value=32, default=42, mandatory=True)
        s_json = json.dumps(s, cls=encode)
        new_s = json.loads(s_json, object_hook=decode)

        self.assertIsInstance(new_s.value, str)
        self.assertIsInstance(new_s.default, str)

        self.assertEqual(new_s.value, s.value)
        self.assertEqual(new_s.default, s.default)
        self.assertEqual(new_s.mandatory, s.mandatory)

class TestJsonEncodeIntegerField(unittest.TestCase):
    def test_encode_integerfield(self):
        s = IntegerField(value=24, default=42, mandatory=True)
        s_json = json.dumps(s, cls=encode)
        new_s = json.loads(s_json, object_hook=decode)

        self.assertIsInstance(new_s.value, int)
        self.assertIsInstance(new_s.default, int)

        self.assertEqual(new_s.value, s.value)
        self.assertEqual(new_s.default, s.default)
        self.assertEqual(new_s.mandatory, s.mandatory)

    def test_encode_cast_integerield(self):
        s = IntegerField(value="42", default="24", mandatory=True)
        s_json = json.dumps(s, cls=encode)
        new_s = json.loads(s_json, object_hook=decode)

        self.assertIsInstance(new_s.value, int)
        self.assertIsInstance(new_s.default, int)

        self.assertEqual(new_s.value, s.value)
        self.assertEqual(new_s.default, s.default)
        self.assertEqual(new_s.mandatory, s.mandatory)
