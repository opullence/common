from ..facts.utils import is_fact_or_composite
from ..patterns import JsonSerializable, is_composite
from ..timer import Clock
from ..utils import generate_uuid, hex_to_uuid, is_list
from .status import StatusCode


class Composable(JsonSerializable):
    def __init__(self, data=None, **kwargs):
        self.data = data

    @property
    def data(self):
        return self._data

    def __eq__(self, other):
        if not isinstance(other, Composable):
            return False
        s_items = self.get(force_array=True)
        o_items = other.get(force_array=True)
        for s, o in zip(s_items, o_items):
            if s != o:
                return False
        return True

    @data.setter
    def data(self, data):
        if is_fact_or_composite(data):
            self._data = data
        else:
            self._data = None

    def get(self, force_array=False):
        if is_composite(self.data):
            return self.data.elements
        if force_array:
            return [] if not self.data else [self.data]
        else:
            return self.data


class Result(JsonSerializable):
    def __init__(
        self,
        input=None,
        output=None,
        status=StatusCode.undefined,
        identifier=None,
        clock=None,
        **kwargs
    ):
        if identifier is None:
            self.identifier = generate_uuid()
        else:
            self.identifier = identifier

        if clock is None:
            self.clock = Clock()
        else:
            self.clock = clock

        self.input = input
        self.output = output
        self.status = status

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, input):
        self._input = Composable(input)

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, output):
        self._output = output if is_list(output) else [output]

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        try:
            statusCode, error = status
        except TypeError:
            self._status = {
                "status": status,
                "code": StatusCode.code_to_label(status),
                "error": None,
            }
        else:
            self._status = {
                "status": statusCode,
                "code": StatusCode.code_to_label(statusCode),
                "error": error,
            }

    def to_json(self):
        obj_dict = super().to_json()
        obj_dict.update(
            {
                "_input": None,
                "_output": None,
                "identifier": self.identifier.hex,
                "input": self.input.get(),
                "output": self.output,
                "clock": self.clock.to_json(),
                "status": (int(self.status["status"]), self.status["error"])
            }
        )
        return obj_dict

    @staticmethod
    def from_json(json_dict):
        json_dict.update(
            {
                "identifier": hex_to_uuid(json_dict["identifier"]),
                "clock": Clock.from_json(json_dict["clock"]),
            }
        )
        return super(Result, Result).from_json(json_dict)
