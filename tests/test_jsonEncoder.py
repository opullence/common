import json
import unittest

from opulence.common.bases.baseFact import BaseFact
from opulence.common.fields import IntegerField, StringField
from opulence.common.job import Composable, Result
from opulence.common.jsonEncoder import decode, encode


class FactA(BaseFact):
    _name_ = "x"
    _description_ = "xx"
    _author_ = "xxx"
    _version_ = 1

    def setup(self):
        self.a = IntegerField(mandatory=False)
        self.b = StringField(default="b")
        self.c = StringField(default="c")


class FactB(BaseFact):
    _name_ = "x"
    _description_ = "xx"
    _author_ = "xxx"
    _version_ = 1

    def setup(self):
        self.a = IntegerField(mandatory=False)
        self.b = StringField(default="b")
        self.c = StringField(default="c")


class TestJsonEncodeJob(unittest.TestCase):
    def test_encode_simple_job(self):
        r = Result(input=FactA(), output=FactB())
        r_json = r.to_json()
        new_r = Result.from_json(r_json)
        self.assertEqual(r.identifier, new_r.identifier)
        self.assertEqual(r.input.get(), new_r.input.get())
        self.assertEqual(r.output.get(), new_r.output.get())
        self.assertEqual(
            type(r.output.get().a.value), type(new_r.output.get().a.value), int
        )
        self.assertEqual(r.clock.start_date, new_r.clock.start_date)
        self.assertEqual(r.clock.end_date, new_r.clock.end_date)

    def test_encode_complex_job(self):
        r = Result()
        r.input = FactA(a="42", b=2)
        r.output = FactB(a="42", b=2)
        r.clock.start()
        r_json = r.to_json()
        new_r = Result.from_json(r_json)
        self.assertEqual(r.identifier, new_r.identifier)
        self.assertEqual(r.input.get(), new_r.input.get())
        self.assertEqual(r.output.get(), new_r.output.get())
        self.assertEqual(
            type(r.output.get().a.value), type(new_r.output.get().a.value), int
        )
        self.assertEqual(r.clock.start_date, new_r.clock.start_date)
        self.assertEqual(r.clock.end_date, new_r.clock.end_date)

    def test_encode_job_using_json(self):
        r = Result()
        r.input = FactA(a="42", b=2)
        r.output = FactB(a="42", b=2)
        r.clock.start()
        r_json = json.dumps(r, cls=encode)
        new_r = json.loads(r_json, object_hook=decode)
        self.assertEqual(r.identifier, new_r.identifier)
        self.assertEqual(r.input.get(), new_r.input.get())
        self.assertEqual(r.output.get(), new_r.output.get())
        self.assertEqual(
            type(r.output.get().a.value), type(new_r.output.get().a.value), int
        )
        self.assertEqual(r.clock.start_date, new_r.clock.start_date)
        self.assertEqual(r.clock.end_date, new_r.clock.end_date)


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
