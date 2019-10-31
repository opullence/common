from ..patterns import JsonSerializable

class BaseField(JsonSerializable):
	def __init__(self, value=None, default=None, mandatory=False, **kwargs):
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