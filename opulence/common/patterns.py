import importlib


from .utils import is_list

class Composite:
    def __init__(self, *args):
        self._elements = []
        for a in args:
            if is_list(a):
                self._elements.extend(a)
            else:
                self._elements.append(a)

    def __add__(self, other):
        return list(set(self.elements + other.elements))

    @property
    def elements(self):
        return self._elements

    def add(self, element):
        self._elements.append(element)

    def remove(self, element):
        self._elements.remove(element)

class JsonSerializable():
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


class SingletonMetaClass(type):
    _instances_ = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances_:
            cls._instances_[cls] = super(SingletonMetaClass, cls).__call__(
                *args, **kwargs
            )
        return cls._instances_[cls]


Singleton = SingletonMetaClass("Singleton", (object,), {})