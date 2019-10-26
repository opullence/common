from .utils import is_list


class SingletonMetaClass(type):
    _instances_ = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances_:
            cls._instances_[cls] = super(SingletonMetaClass, cls).__call__(
                *args, **kwargs
            )
        return cls._instances_[cls]


Singleton = SingletonMetaClass("Singleton", (object,), {})


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
