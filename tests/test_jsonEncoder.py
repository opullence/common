import json
import unittest

from opulence.common.bases.baseFact import BaseFact
from opulence.common.fields import IntegerField, StringField
from opulence.common.job import Result
from opulence.common.jsonEncoder import decode, encode
from opulence.common.timer import Clock


class F(BaseFact):
    _name_ = "xx"
    _description_ = "xx"
    _author_ = "xx"
    _version_ = 1

    def setup(self):
        self.a = IntegerField()
        self.b = StringField(default="b")
        self.c = StringField(default="c")


class TestJsonEncodeClock(unittest.TestCase):
    def test_encode_simple_unstarted_clock(self):
        clock_a = Clock()
        a_json = clock_a.to_json()
        new_a = Clock.from_json(a_json)

        self.assertEqual(clock_a.start_date, new_a.start_date)
        self.assertEqual(clock_a.end_date, new_a.end_date)
        self.assertEqual(clock_a.started, new_a.started, False)
        # self.assertRaises(clock_a.time_elapsed)

    def test_encode_simple_started_clock(self):
        clock_a = Clock()
        clock_a.start()

        clock_a.start()

        a_json = clock_a.to_json()
        new_a = Clock.from_json(a_json)

        self.assertEqual(clock_a.start_date, new_a.start_date)
        self.assertEqual(clock_a.end_date, new_a.end_date)
        self.assertEqual(clock_a.started, new_a.started, True)
        self.assertLess(clock_a.time_elapsed, new_a.time_elapsed)


class TestJsonEncodeResult(unittest.TestCase):
    def test_encode_simple_result(self):
        fact_a = F(a=42, b="bb", c="cc")
        fact_b = F(a=84, b="bbbb", c="cccc")

        res = Result(input=fact_a, output=fact_b)
        res.status = 42
        res.clock.start()
        res.clock.stop()

        res_json = json.dumps(res, cls=encode)
        new_res = json.loads(res_json, object_hook=decode)

        for a, b in zip(
            res.output.get(force_array=True), new_res.output.get(force_array=True)
        ):
            self.assertEqual(a, b)
        for a, b in zip(
            res.input.get(force_array=True), new_res.input.get(force_array=True)
        ):
            self.assertEqual(a, b)
        self.assertEqual(res.status, new_res.status)
        self.assertEqual(res.identifier, new_res.identifier)
        self.assertEqual(res.clock.time_elapsed, new_res.clock.time_elapsed)

    def test_encode_invalid_result(self):
        fact_a = F(a=42, b="b", c="c")
        res = Result()
        res.input = fact_a
        res.status = 404, "Not found"
        res.output = "Whynot"
        res.clock.start()
        res.clock.stop()
        res_json = json.dumps(res, cls=encode)
        new_res = json.loads(res_json, object_hook=decode)

        self.assertEqual(res.identifier, new_res.identifier)
        self.assertEqual(res.input.get(), new_res.input.get())
        self.assertEqual(res.output.get(), new_res.output.get())
        self.assertIsNone(new_res.output.get())
        self.assertEqual(res.clock.time_elapsed, new_res.clock.time_elapsed)
        self.assertIsNone(res.output.get(), new_res.output.get())


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
