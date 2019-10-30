import importlib

from ..plugins.basePlugin import BasePlugin
from ..plugins.exceptions import PluginFormatError
from ..fields import BaseField


class BaseFact(BasePlugin):

    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, **kwargs):
        self.setup()
        for key, value in kwargs.items():
            if key in self.__dict__:
                self.__dict__[key].value = value
        super().__init__()

    def __hash__(self):
        val = 0
        print(self.__dict__)
        for f in self.__dict__:
            val += hash(self.__dict__[f].value)
        if val == 0:
            return id(self)
        return val

    def __eq__(self, other):
        zip_fields = [[self.__dict__[s], other.__dict__[o]]
                      for s, o in zip(self.__dict__, other.__dict__)]
        toto = all(
            [False if s.value != o.value else True for s, o in zip_fields])
        return (
            self.__class__ == other.__class__ and
            all([False if s.value != o.value else True for s, o in zip_fields])
        )

    def setup(self):
        pass

    @property
    def plugin_category(self):
        return BaseFact.__name__

    def is_valid(self):
        for _, f in self.get_fields().items():
            if f.mandatory and f.value is None:
                return False
        return True

    def get_fields(self):
        return {
            field: self.__dict__[field] for field in self.__dict__ if isinstance(
                self.__dict__[field], BaseField)}

    def get_info(self):
        fields = []
        for key, data in self.get_fields().items():
            fields.append({"name": key,
                           "mandatory": data.mandatory})
        data = {"fields": fields}
        return {**super().get_info(), **data}

    def to_json(self):
        obj_dict = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__
        }
        obj_dict.update(self.__dict__)
        return obj_dict

    @staticmethod
    def from_json(json_dict):
        if "__class__" in json_dict:
            class_name = json_dict.pop("__class__")
            module_name = json_dict.pop("__module__")
            module = importlib.import_module(module_name)
            _class = getattr(module, class_name)
            obj = _class(**json_dict)
        else:
            obj = json_dict
        return obj