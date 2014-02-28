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

Validating without network access
=================================

To maximise code re-use, individual schema files reference other
schema files.  In the example above, `schema/appliance_group.json` is
loaded from the local disk and then all files referred to from
`schema/appliance_group.json` are loaded from github.

If you need to do validation without network
access then it should be possible but will require a bit of hacking.
I think you would first need to remove all the "id" properties from
every schema file and then use a code snippet like
[this one](https://github.com/Julian/jsonschema/issues/98#issuecomment-17531405).
