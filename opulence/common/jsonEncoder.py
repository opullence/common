import json
from datetime import datetime
from time import mktime

from .bases.baseFact import BaseFact
from .fields import BaseField
from .job import Composable, Result


class encode(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Result):
            return {"__type__": "__result__", "result": obj.to_json()}
        elif isinstance(obj, BaseFact):
            return {"__type__": "__basefact__", "fact": obj.to_json()}
        elif isinstance(obj, Composable):
            return {"__type__": "__composable__", "composable": obj.to_json()}
        elif isinstance(obj, BaseField):
            return {"__type__": "__basefield__", "field": obj.to_json()}
        elif isinstance(obj, datetime):
            return {"__type__": "__datetime__", "epoch": int(mktime(obj.timetuple()))}
        return json.JSONEncoder.default(self, obj)


def decode(obj):
    if "__type__" in obj:
        if obj["__type__"] == "__result__":
            return Result.from_json(obj["result"])
        elif obj["__type__"] == "__composable__":
            return Composable.from_json(obj["composable"])
        elif obj["__type__"] == "__basefact__":
            return BaseFact.from_json(obj["fact"])
        elif obj["__type__"] == "__basefield__":
            return BaseField.from_json(obj["field"])
        elif obj["__type__"] == "__datetime__":
            return datetime.fromtimestamp(obj["epoch"])
    return obj


def custom_dumps(obj):
    return json.dumps(obj, cls=encode)


def custom_loads(obj):
    return json.loads(obj, object_hook=decode)
