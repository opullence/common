from ..bases import BaseFact
from ..patterns import Composite


def is_fact_or_composite(obj):
	return isinstance(obj, Composite) or isinstance(obj, BaseFact)

def is_composite(obj):
	return isinstance(obj, Composite)
