from .status import StatusCode

from .utils import is_fact_or_composite, is_composite
from ..utils import generate_uuid
from ..timer import Clock

class Composable:
    def __init__(self, data=None):
        self.data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if is_fact_or_composite(data):
            self._data = data

        
    def get(self):
        if is_composite(self.data):
            return self.data.elements
        return [self.data]


class Result:
    def __init__(self, input=None, output=None):
        self.id = generate_uuid()
        self.input = input
        self.output = output

        self.error = None
        self.status = StatusCode.undefined

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
        print(status)
        try:
            statusCode, error = status
        except TypeError:
            self._status = {
                'status': status,
                'code': StatusCode.code_to_label(status),
                'error': None
            }
        else:
            self._status = {
                'status': statusCode,
                'code': StatusCode.code_to_label(statusCode),
                'error': error
            }