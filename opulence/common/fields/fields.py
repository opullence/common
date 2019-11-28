from .baseField import BaseField


class StringField(BaseField):
    def cast_value(self, value):
        return str(value)


class IntegerField(BaseField):
    def cast_value(self, value):
        return int(value)


class DynamicField(BaseField):
    pass
