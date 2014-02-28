NILM METADATA
=============

NILM Metadata is a [JSON Schema](http://json-schema.org/) for
modelling appliances, meters, measurements, buildings and datasets.
Default properties for appliances and meters are also provided.


Validating a new JSON file against the schema
=============================================

```python
from jsonschema import validate
import json
validate(json.load(open('examples/appliance_group.json')),
         json.load(open('schema/appliance_group.json')))
```

Development plans
=================

* Ultimately, it might be nice if both the schema and the defaults
  were specified on a semantic wiki, which would make it easier to
  search and modify.  See
  [this blog post for more details](http://jack-kelly.com/wiki_and_online_community_for_electricity_disaggregation).

* At the moment, the schema allows unknown properties.  This is bad.
  It appears we can't use `"additionalProperties": false` because this
  prevents extension.  So let's wait for the "ban unknown properties
  (v5 proposal) to be implemented".  See
  [this issue on jsonschema](https://github.com/Julian/jsonschema/issues/150).


Related projects
================

* [Project Haystack](http://project-haystack.org/), to quote their
  website, "*is an open source initiative to develop tagging
  conventions and taxonomies for building equipment and operational
  data. We define standardized data models for sites, equipment, and
  points related to energy, HVAC, lighting, and other environmental
  systems.*"  Haystack is an awesome project but it does not specify a
  controlled vocabulary for appliances, which is the meat of the
  `nilm_metadata` project.  Where appropriate, `nilm_metadata` does
  use similar properties to Haystack (e.g. the "site_meter" property
  is borrowed directly from Haystack).


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
