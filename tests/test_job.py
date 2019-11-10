import unittest
import json

from opulence.common.facts import BaseFact
from opulence.common.fields import IntegerField, StringField
from opulence.common.job import Result, StatusCode
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


class TestJobResult(unittest.TestCase):

    def test_job_result_started(self):
        a = FactA()
        j = Result(input=a)

        j.status = StatusCode.finished
        j_json = json.dumps(j, cls=encode)
        new_j = json.loads(j_json, object_hook=decode)

        self.assertEqual(False, StatusCode.is_errored(new_j.status["status"]), StatusCode.is_errored(j.status["status"]))
        self.assertEqual(j.status, new_j.status)
        self.assertEqual("Finished", j.status["code"], new_j.status["code"])


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
