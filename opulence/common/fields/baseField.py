import importlib


class BaseField():
	def __init__(self, value=None, default=None, mandatory=False):
		self._default = default
		self._mandatory = mandatory
		self._value = value

	def __repr__(self):
		return 'value: {}, default: {}, mandatory: {}'.format(self.value, self._default, self._mandatory)

	def __hash__(self):
		return hash(self.value)


	def __eq__(self, other):
		return (
			self.__class__ == other.__class__ and
			self.value == other.value
		)

	@property
	def mandatory(self):
		return self._mandatory

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, v):
		self._value = v


	def to_json(self):
		obj_dict = {
			"__class__": self.__class__.__name__,
			"__module__": self.__module__
		}
		obj_dict.update({
			"value": self.value,
			"mandatory": self.mandatory,
			"default": self._default
		})
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