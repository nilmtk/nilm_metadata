NILM METADATA
=============

NILM Metadata (where 'NILM' stands for 'non-instrusive load
monitoring') is a metadata framework for describing appliances, meters,
measurements, buildings and datasets.

Please jump in and add to or modify the schema and documentation!

### Documentation

The
[documentation is available online](http://nilm-metadata.readthedocs.org).

If you're new to NILM Metadata then please read this README and then
dive into the [tutorial](http://nilm-metadata.readthedocs.org/en/latest/tutorial.html)
to find out how 
to see a worked example.

Or, if you are already familiar with NILM Metadata then perhaps you
want direct access to the full description of the
"[Dataset metadata](http://nilm-metadata.readthedocs.org/en/latest/dataset_metadata.html)".

## There are two sides to NILM Metadata:

### 1) A schema describing energy datasets

Modelled objects include:

* electricity meters (whole-home and individual appliance meters)
  * wiring hierarchy of meters
  * a controlled vocabulary for measurement names
  * description of pre-processing applied
  * storage of pre-processed statistics
* domestic appliances
  * a controlled vocabulary for appliance names
  * each appliance can contain any number of components (e.g. a
    light fitting can contain multiple lamps and a dimmer)
  * a list of time periods when each appliance was active
  * manufacturer, model, nominal power consumption etc.
* a mapping of which appliances are connected to which meters
* buildings
* datasets 

The metadata itself can be either
[YAML](http://en.wikipedia.org/wiki/YAML) or JSON.

### 2) Central metadata

Common info about appliances is stored in NILM Metadata.  This includes:

* Categories for each appliance type
* prior knowledge about the distribution of variables such as:
  * on power
  * on duration
  * usage in terms of hour per day
  * appliance correlations (e.g. that the TV is usually on if the
    games console is on)
* valid additional properties for each appliance
* mapping from country codes to nominal mains voltage ranges

The common info about appliances uses a simple but powerful
inheritance mechanism to allow appliances to inherit from a other
appliances.  For example, `laptop computer` is a specialisation of
`computer` and the two share several properties (e.g. both are in the
`ICT` category).  So `laptop computer` inherits from `computer` and
modifies and adds any properties it needs.  In this way, we can
embrace the
["don't repeat yourself (DRY)"](http://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
principal by exploiting the relationship between appliances.

### Python utilities

NILM Metadata comes with a Python module which collects all 
ApplianceTypes in `central_metadata/appliance_types/*.yaml`,
performs inheritance and instantiates components and
returns a dictionary where each key is an ApplianceType name and each
value is an ApplianceType dict.  Here's how to use it:

```python
from nilm_metadata import get_appliance_types
appliance_types = get_appliance_types()
```

NILM Metadata also comes with a `convert_yaml_to_hdf5()` function
which will convert a YAML instance of NILM Metadata to the HDF5 file
format.

## Research paper describing NILM metadata

The following paper describes NILM metadata in detail:

* Jack Kelly and William Knottenbelt (2014). **Metadata for Energy
  Disaggregation**. In The 2nd IEEE International Workshop on Consumer
  Devices and Systems (CDS 2014) in Västerås, Sweden.
  arXiv:[1403.5946](http://arxiv.org/abs/1403.5946)
  DOI:[10.1109/COMPSACW.2014.97](http://dx.doi.org/10.1109/COMPSACW.2014.97)

Bibtex:

```
@inproceedings{NILM_Metadata,
title = {{Metadata for Energy Disaggregation}},
author = {Kelly, Jack and Knottenbelt, William},
year = {2014},
month = jul,
address = {V{\" a}ster{\aa}s, Sweden},
booktitle = {The 2nd IEEE International Workshop on Consumer Devices and Systems (CDS 2014)},
archivePrefix = {arXiv},
arxivId = {1403.5946},
eprint = {1403.5946},
doi = {10.1109/COMPSACW.2014.97}
}
```

Please cite this paper if you use NILM metadata in academic research.
But please also be aware that the online documentation is more
up-to-date than the paper.


## JSON Schema has been depreciated

In
[version 0.1 of the schema](https://github.com/nilmtk/nilm_metadata/tree/v0.1.0),
we wrote a very comprehensive (and complex) schema using
[JSON Schema](http://json-schema.org/) in order to automate the
validation of metadata instances.  JSON Schema is a lovely language
and can capture everything we need but, because our metadata is quite
comprehensive, we found that using JSON Schema was a significant time
drain and made it hard to move quickly and add new ideas to the
metadata.  As such, when we moved from v0.1 to v0.2, the JSON Schema
has been dropped.  Please use the
[human-readable documentation](http://nilm-metadata.readthedocs.org)
instead.  If there is a real desire for automated validation then we
could resurrect the JSON Schema, but it is a fair amount of work to
maintain.

However, there are YAML validators freely available to make sure you are 
using the correct YAML format.  For example: [YAMLlint](http://www.yamllint.com)


Installation
============

If you want to use the Python package in order to concatenate the
common appliance metadata then please run:

```
sudo python setup.py develop
```

Please do *not* use `python setup.py install` until I have updated
`setup.py` to copy the relevant `*.yaml` files.  See [issue #6](https://github.com/nilmtk/nilm_metadata/issues/6).

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
* [WikiEnergy](http://wiki-energy.org/) "*A Universe of Energy Data,
  Available Around the World*".
* [sMAP metadata tags](http://www.eecs.berkeley.edu/~stevedh/smap2/tags.html)
  - sMAP is Berkley's "Simple Measurement and Actuation Profile".
