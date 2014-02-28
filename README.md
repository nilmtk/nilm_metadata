NILM Schema
===========

[JSON Schema](http://json-schema.org/) for modelling meters, measurements, appliances, buildings etc


Validating a new JSON file against the schema
=============================================

```python
from jsonschema import validate
import json
validate(json.load(open('examples/appliance_group.json')),
         json.load(open('schema/appliance_group.json')))
```


Testing
=======

```
./test.py
```
