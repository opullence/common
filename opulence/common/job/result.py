from ..patterns import JsonSerializable
from ..timer import Clock
from ..utils import generate_uuid, hex_to_uuid
from .status import StatusCode
from .utils import is_composite, is_fact_or_composite


class Composable(JsonSerializable):
    def __init__(self, data=None, **kwargs):
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if is_fact_or_composite(data):
            self._data = data
        else:
            self._data = None

    def get(self, force_array=False):
        if is_composite(self.data):
            return self.data.elements
        return [self.data] if force_array else self.data


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
        self._output = Composable(output)

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
                "identifier": self.identifier.hex,
                "input": self.input.get(),
                "output": self.output.get(),
                "clock": self.clock.to_json(),
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
