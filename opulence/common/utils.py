import uuid


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
