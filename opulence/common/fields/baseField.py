class BaseField():
	def __init__(self, default=None, mandatory=False):
		self._default = default
		self._mandatory = mandatory
		self._value = None

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
		return str(self.value)