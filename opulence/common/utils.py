import uuid
from datetime import datetime

import dateutil.parser


def datetime_to_string(date: datetime):
    return date.isoformat()


def string_to_datetime(s: str):
    return dateutil.parser.parse(s)


def hex_to_uuid(hex: str):
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
