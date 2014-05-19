NILM METADATA
=============

NILM Metadata (where `NILM' stands for `non-instrusive load
monitoring') is a metadata framework for describing appliances, meters,
measurements, buildings and datasets.

The aim is that NILM Metadata can be used as a stand-alone project to
specify the metadata for any NILM dataset; and that metadata can then
be used with the open-source energy disaggregation and analytics
framework [NILMTK](http://nilmtk.github.io/).

Please jump in and add to or modify the schema and documentation!

There are two sides to NILM Metadata:

### 1) A schema for  metadata that is included with disaggregated energy datasets

The schema covers:

* electricity meters (whole-home and individual appliance meters)
  * wiring hierarchy of meters
  * a controlled vocabulary for measurement names
* domestic appliances
  * a controlled vocabulary for appliance names
  * each appliance can contain any number of components (e.g. a
    light fitting can contain multiple lamps and a dimmer)
  * a list of time periods when each appliance was active
* a mapping of which appliances are connected to which meters
* buildings
* datasets

The metadata itself can be either
[YAML](http://en.wikipedia.org/wiki/YAML) or JSON.

### 2) Common information about appliances

Common info about appliances is stored in NILM Metadata.  This includes:

* Categories for each appliance type
* prior knowledge about the distribution of variables such as:
  * on power
  * on duration
  * usage in terms of hour per day
  * appliance correlations (e.g. that the TV is usually on if the
    games console is on)
* valid additional properties for each appliance

The common info about appliances uses a simple but powerful
inheritance mechanism to allow appliances to inherit from a other
appliances.  For example, `laptop computer` is a specialisation of
`computer` and the two share several properties (e.g. both are in the
`ICT` category).  So `laptop computer` inherits from `computer` and
modifies and adds any properties it needs.  In this way, we can
embrace the
["don't repeat yourself (DRY)"](http://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
principal by exploiting the relationship between appliances.

## Research paper describing NILM metadata

The following paper describes NILM metadata in detail:

* Jack Kelly and William Knottenbelt (2014). **Metadata for Energy
  Disaggregation**. In The 2nd IEEE International Workshop on Consumer
  Devices and Systems (CDS 2014) in Västerås, Sweden.
  [arXiv:1403.5946](http://arxiv.org/abs/1403.5946)

Please cite this paper if you use NILM metadata.

## JSON Schema has been depreciated

In order to automate the validation of metadata instances, we did
write a very comprehensive (and complex) schema using JSON Schema.
JSON Schema is a lovely language and can capture everything we need
but, because our metadata is quite comprehensive, we found that using
JSON Schema was a significant time drain and made it hard to move
quickly and add new ideas to the metadata.  As such, when we moved
from v0.1 to v0.2, the JSON Schema has been depreciated.  Please use
the human-readable documentation instead.  If there is a real desire
for automated validation then we could resurrect the JSON Schema, but
it is a fair amount of work to maintain, and is a little fragile.

## Examples

### Example of dataset metadata

dataset.yaml
```
name: UK-DALE
long_name: UK Domestic Appliance-Level Electricity
mains_voltage:
  nominal: 230
  upper_limit: 253
  lower_limit: 215
```

meter_devices.yaml
```
- model: EnviR
  manufacturer: Current Cost
  measurements:
  - physical_quantity: power
    ac_type: apparent
    lower_limit: 0
    upper_limit: 30000
```

building1.yaml
```
instance: 1
rooms:
- {name: kitchen, instance: 1}
- {name: lounge, instance: 1}
geo_location:
  locality: London
  country: GB
  latitude: 51.464462
  longitude: -0.076544
timezone: Europe/London
timeframe:
  start: 2012-11-09
  end: 2014-03-11
elec_meters: # Metadata about appliances

# Meter that measures whole-house mains:
- instance: 1
  device_model: EnviR
  site_meter: true
  sensors:
  - data_location: house1/channel_1.dat

# Meter that measures lighting circuit:
- instance: 2
  device_model: EnviR
  submeter_of: 1
  sensors:
  - data_location: house1/channel_2.dat

# Meter that measures kitchen lights:
- instance: 3
  device_model: EnviR
  submeter_of: 2
  sensors:
  - data_location: house1/channel_2.dat
  preprocessing:
  - {filter: clip, maximum: 4000}
  appliances:
  - type: light
    components:
    - type: LED lamp
      count: 10
      nominal_consumption: {on_power: 10}
      manufacturer: Philips
      year_of_manufacture: 2011
    - type: dimmer
    on_power_threshold: 10
    main_room_light: true
    dates_active:
    - {start: 2012, end: 2013}
```

### Example of common metadata

To demonstrate the inheritance system, let's look at specifying a
boiler.

First, NILM Metadata specifies a `heating appliance` object, which is
can be considered the "base class":

```yaml
heating appliance:
  parent: appliance
  categories:
    traditional: heating
    size: large
```

Next, we specify a `boiler` object, which inherits from `heating appliance`:

```yaml
#------------- BOILERS ------------------------

boiler: # all boilers except for electric boilers

  parent: heating appliance

  synonyms: [furnace]

  # Categories of the child object are appended
  # to existing categories in the parent.
  categories:
    google_shopping:
      - climate control
      - furnaces and boilers

  # Here we specify that boilers have a component
  # which is itself an object whose parent
  # is `water pump`.
  components:
    - parent: water pump

  # Boilers have a property which most other appliances
  # do not have: a fuel source.  We specify additional
  # properties using the JSON Schema syntax.
  additional_properties:
    fuel:
      enum: [natural gas, coal, wood, oil, LPG]
      
  subtypes:
    - combi
    - regular

  # We can specify the different mechanisms that
  # control the boiler.  This is useful, for example,
  # if we want to find all appliances which 
  # must be manually controlled (e.g. toasters)
  control: [manual, timer, thermostat]

  # We can also declare prior knowledge about boilers.
  # For example, we know that boilers tend to be in
  # bathrooms, utility rooms or kitchens
  distributions:
    room:
      distribution_of_data:
        categories: [bathroom, utility, kitchen]
        values: [0.3, 0.2, 0.2]
        # If the values do not add to 1 then the assumption
        # is that the remaining probability mass is distributed equally to
        # all other rooms.
      source: subjective # These values are basically guesses!
```


Finally, in the metadata for the dataset itself, we can do:


```yaml

  type: boiler
  manufacturer: Worcester
  model: Greenstar 30CDi Conventional natural gas
  room:
    name: bathroom
    instance: 1
  year_of_purchase: 2011
  fuel: natural gas
  subtype: regular
  part_number: 41-311-71
  efficiency_rating: 
    certification_name: SEDBUK
    rating: A
  nominal_consumption:
    on_power: 70
  distributions:
    on_power:
    - model:
        distribution_name: normal
        mu: 73
        sigma: 12
```


Version numbering and contributing
==================================

The current release is version 0.2.0.  There are definitely plenty of
improvements that can be made so please submit pull requests for the
dev version!

Installation
============

```
sudo python setup.py install
```

Or, if you want to develop:

```
sudo python setup.py install
```


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
