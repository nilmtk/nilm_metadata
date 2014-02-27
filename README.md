NILM Schema
===========

JSON-Schema for modelling meters, measurements, appliances, buildings etc

Testing
=======

```python
from jsonschema import validate
import json
validate(json.load(open('examples/appliance_group.json')),
         json.load(open('schema/appliance_group.json')))
```
