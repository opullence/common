from .baseField import BaseField

class StringField(BaseField):
	@BaseField.value.setter
	def value(self, v):
		self._value = str(v)		


class IntegerField(BaseField):
	@BaseField.value.setter
	def value(self, v):
		self._value = int(v)

# this is just an example, it's not usefull since integers are already json serializable
	def to_json(self):
		obj_dict = super().to_json()

		obj_dict.update({
			"value": str(self.value),
		})
		return obj_dict

	@staticmethod
	def from_json(json_dict):
		json_dict.update({
			"value": int(json_dict["value"])
		})
		return super(IntegerField, IntegerField).from_json(json_dict)