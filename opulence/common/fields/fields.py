from .baseField import BaseField

class StringField(BaseField):
	@BaseField.value.setter
	def value(self, v):
		self._value = str(v)		


class IntegerField(BaseField):
	@BaseField.value.setter
	def value(self, v):
		self._value = int(v)