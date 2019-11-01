from ..job import Result, StatusCode
from ..patterns import Composite
from ..plugins import BasePlugin
from ..plugins.exceptions import PluginFormatError
from ..utils import is_list
from .baseFact import BaseFact


class BaseCollector(BasePlugin):
    _allowed_input_ = ()
    _active_scanning_ = False

    def __init__(self, *args, **kwargs):
        if not self._allowed_input_:
            raise PluginFormatError(
                f"<{type(self).__name__}> needs at least one allowed_input"
            )
        super().__init__()

    @property
    def plugin_category(self):
        return BaseCollector.__name__

    @property
    def allowed_input(self):
        return self._allowed_input_

    def run(self, facts):
        result = Result(input=facts)

        if result.input is None:
            result.status = StatusCode.empty, "No input provided"
            return result
        try:
            # result.executionClock.start()
            result.status = StatusCode.started

            #result.output = self._sanitize_output(self.launch(result.input.get()))
            result.output = self.launch(result.input.get())
            # result.executionClock.stop()
            result.status = StatusCode.finished

        except Exception as err:
            result.status = StatusCode.error, str(err)
            print("!!!!!!!!!!!!")
            print("Error in run():", err)
            print("!!!!!!!!!!!!")
        finally:
            print("Run output:", result.output, result.output.get())
            return result

    @staticmethod
    def _sanitize_output(output):
        if not is_list(output):
            output = [output]
        return [ o for o in output if isinstance(o, BaseFact) ] # and o.is_valid()]

    def launch(self, fact):
        raise NotImplementedError(
            f"Method launch() should be defined for Plugin <{type(self).__name__}>"
        )

    def get_allowed_input_as_list(self):
        ret = []
        for input in self.allowed_input:
            if isinstance(input, Composite):
                ret.append([i.__name__ for i in input.elements])
            else:
                ret.append([input.__name__])
        return ret

    def get_info(self):
        data = {
            "active_scanning": self._active_scanning_,
            "allowed_input": self.get_allowed_input_as_list(),
        }
        return {**super().get_info(), **data}
