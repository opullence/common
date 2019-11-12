import unittest
import json

from opulence.common.facts import BaseFact
from opulence.common.fields import IntegerField, StringField
from opulence.common.job import Result, StatusCode, Composable
from opulence.common.jsonEncoder import decode, encode
from opulence.common.patterns import Composite


class FactA(BaseFact):
    _name_ = "x"
    _description_ = "xx"
    _author_ = "xxx"
    _version_ = 1

    def setup(self):
        self.a = IntegerField(mandatory=False)
        self.b = StringField(default="b")
        self.c = StringField(default="c")

class TestComposables(unittest.TestCase):
    def test_composable_eq(self):
        a = FactA(a=1)
        b = FactA(a=2)
        c = Composable(Composite(a, b))

        a1 = FactA(a=1)
        b1 = FactA(a=2)
        c1 = Composable(Composite(a1, b1))

        self.assertTrue(c == c1)

    def test_composable_eq_2(self):
        a = FactA(a=1)
        c = Composable(Composite(a))

        a1 = FactA(a=1)
        c1 = Composable(a1)
        
        self.assertTrue(c == c1)

    def test_composable_not_eq(self):
        a = FactA(a=1)
        b = FactA(a=2)
        c = Composable(Composite(a, b))

        a1 = FactA(a=1)

        self.assertTrue(c != a1)

    def test_composable_not_eq_2(self):
        a = FactA(a=1)
        b = FactA(a=2)
        c = Composable(Composite(a, b))

        a1 = FactA(a=1)
        b1 = FactA(a=4242)
        c1 = Composable(Composite(a1, b1))

        self.assertTrue(c != c1)

class TestJobResult(unittest.TestCase):

    def test_job_result_composite(self):
        a = FactA()
        b = FactA()
        j = Result(input=Composite(a, b))

        j.status = StatusCode.finished
        j_json = json.dumps(j, cls=encode)
        new_j = json.loads(j_json, object_hook=decode)

        self.assertEqual(False, StatusCode.is_errored(new_j.status["status"]), StatusCode.is_errored(j.status["status"]))
        self.assertEqual(j.status, new_j.status)
        self.assertEqual("Finished", j.status["code"], new_j.status["code"])
        self.assertEqual(j.input, new_j.input)

    def test_job_result_error_msg(self):
        a = FactA()
        j = Result(input=a)

        j.status = StatusCode.finished, "this is an error"
        j_json = json.dumps(j, cls=encode)
        new_j = json.loads(j_json, object_hook=decode)

        self.assertEqual(False, StatusCode.is_errored(new_j.status["status"]), StatusCode.is_errored(j.status["status"]))
        self.assertEqual(j.status, new_j.status)
        self.assertEqual("Finished", j.status["code"], new_j.status["code"])
        self.assertEqual("this is an error", j.status["error"], new_j.status["error"])

    def test_job_result_errored(self):
        a = FactA()
        j = Result(input=a)

        j.status = StatusCode.error
        j_json = json.dumps(j, cls=encode)
        new_j = json.loads(j_json, object_hook=decode)

        self.assertEqual(True, StatusCode.is_errored(new_j.status["status"]), StatusCode.is_errored(j.status["status"]))
        self.assertEqual(j.status, new_j.status)

    def test_job_result_errored_bis(self):
        a = FactA()
        j = Result(input=a)

        j.status = StatusCode.rate_limited
        j_json = json.dumps(j, cls=encode)
        new_j = json.loads(j_json, object_hook=decode)

        self.assertEqual(True, StatusCode.is_errored(new_j.status["status"]), StatusCode.is_errored(j.status["status"]))
        self.assertEqual(j.status, new_j.status)

