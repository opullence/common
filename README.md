# Commons
...


## Playing with jsonEncoder

### With internal API

```python

>>> from opulence.common.bases import BaseFact
>>>
>>> jon = BaseFact()
>>>
>>> jayson = jon.to_json()
>>> new_jon = BaseFact.from_json(jayson)
```

### With json

```python
>>> import json
>>> from opulence.common.bases import BaseFact
>>> from opulence.common.jsonEncoder import encode, decode
>>>
>>> jon = BaseFact()
>>>
>>> jayson = json.dumps(jon, cls=encode)
>>> json.loads(jayson, object_hook=decode)

```

## Test is_fact_or_composite

```python
>>> from opulence.common.job.utils import is_fact_or_composite
>>> from opulence.common.bases import BaseFact
>>> from opulence.common.patterns import Composite
>>>
>>> b = BaseFact()
>>> c = Composite()
>>> is_fact_or_composite(b)
True
>>> is_fact_or_composite(c)
True
>>> is_fact_or_composite(42)
False
```