from .baseField import BaseField


class StringField(BaseField):
    pass

class IntegerField(BaseField):
    def cast_value(self, value):
        return int(value)