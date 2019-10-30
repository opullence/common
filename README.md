# Commons
...


## Playing with jsonEncoder

### Serialize a fact With internal API

```python
>>> from opulence.common.bases import BaseFact
>>>
>>> jon = BaseFact()
>>>
>>> jayson = jon.to_json()
>>> new_jon = BaseFact.from_json(jayson)
```

### Serialize a fact with json module

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


### Serialize a Field

```python
>>> from opulence.common.fields import StringField, IntegerField
>>> un = IntegerField(value="43")
>>> un_json = un.to_json()
>>> deux = IntegerField.from_json(un_json)
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