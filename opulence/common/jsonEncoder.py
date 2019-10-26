import json
from datetime import datetime
from multiprocessing.managers import ListProxy
from time import mktime

from bson import ObjectId
from mongoengine.queryset import QuerySet


class customEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            return obj.to_json()
        elif isinstance(obj, ListProxy):
            return json.loads(obj)
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return {"__type__": "__datetime__", "epoch": int(mktime(obj.timetuple()))}
        return json.JSONEncoder.default(self, obj)


def decode(obj):
    if "__type__" in obj:
        if obj["__type__"] == "__datetime__":
            return datetime.fromtimestamp(obj["epoch"])
    return obj


def custom_dumps(obj):
    return json.dumps(obj, cls=customEncoder)


def custom_loads(obj):
    return json.loads(obj, object_hook=decode)
