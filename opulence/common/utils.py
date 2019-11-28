import uuid
from datetime import datetime

from dateutil.parser import parse


def now():
    return datetime.now()


def datetime_to_str(date: datetime):
    if isinstance(date, datetime):
        return date.isoformat()
    return None


def str_to_datetime(s: str):
    if s is not None:
        return parse(s)
    return None


def hex_to_uuid(hex):
    return uuid.UUID(hex)


def generate_uuid():
    return uuid.uuid4()


def is_iterable(element):
    try:
        iter(element)
    except TypeError:
        return False
    else:
        return True


def is_list(element):
    return isinstance(element, (set, list, tuple))
