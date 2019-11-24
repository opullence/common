import json

from .facts import BaseFact
from .fields import BaseField
from .job import Result


class encode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Result):
            return {"__type__": "__result__", "result": obj.to_json()}
        elif isinstance(obj, BaseFact):
            return {"__type__": "__basefact__", "fact": obj.to_json()}
        elif isinstance(obj, BaseField):
            return {"__type__": "__basefield__", "field": obj.to_json()}
        return json.JSONEncoder.default(self, obj)  # pragma: no cover


def decode(obj):
    if "__type__" in obj:
        if obj["__type__"] == "__result__":
            return Result.from_json(obj["result"])
        elif obj["__type__"] == "__basefact__":
            return BaseFact.from_json(obj["fact"])
        elif obj["__type__"] == "__basefield__":
            return BaseField.from_json(obj["field"])
    return obj


def custom_dumps(obj):
    return json.dumps(obj, cls=encode)


def custom_loads(obj):
    return json.loads(obj, object_hook=decode)
