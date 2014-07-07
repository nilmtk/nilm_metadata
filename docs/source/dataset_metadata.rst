****************
Dataset metadata
****************

This page describes the metadata schema for describing a dataset.

There are two file formats for the metadata: YAML and HDF5.  
YAML metadata files should be in a ``metadata`` folder.
Each section of this doc starts by describing where the relevant
metadata is stored in both file formats.

.. _dataset-schema:

Dataset
-------

This object describes aspects about the entire dataset.  For example,
the name of the dataset, the authors, the geographical location of the
entire dataset etc.

* Location in YAML: ``dataset.yaml``
* Location in HDF5: ``store.root._v_attrs.metadata``

Metadata attributes (some of these attributes are adapted from the
Dublin Core Metadata Initiative or DCMI):

:name: (string) (required) Short name for the dataset.  e.g. 'REDD' or
       'UK-DALE'.  Equivalent DCMI element is 'title'.
:long_name: (string) Full name of the dataset, eg. 'Reference Energy
            Disaggregation Data Set'.
:creators: (list of strings) in the format '<Lastname>,
           <Firstname>'. DCMI element.
:timezone: (string) Please use the standard TZ name from the `IANA
           (aka Olson) Time Zone Database
           <http://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_ 
           e.g. 'America/New_York' or 'Europe/London'.
:publication_date: (string) Related to the 'date' DCMI element.  ISO
                   8601 format.  e.g. '2014-06-23'
:contact: (string) Email address
:institution: (string)
:description: (string) DCMI element.  Human-readable, brief
              description.  e.g. describe sample rate, geo location etc.
:number_of_buildings: (int)
:identifier: (string): A digital object identifier (DOI) or URI for
             the dataset.  DCMI element.
:subject: (string): For example, is this dataset about domestic or
          commercial buildings?  Does it include disaggregated
          appliance-by-appliance data or just whole-building data?
          DCMI element.  Human-readable free text.
:geospatial_coverage: (string): Spatial coverage.  e.g. 'Southern
                      England'. Related to the 'coverage' DCMI
                      element.  Human-readable free text.
:temporal_coverage: (`Interval`_, see below) Start and end dates for
                    the entire dataset.
:funding: (list of strings) A list of all the sources of funding used
          to produce this dataset.
:publisher: (string) The entity responsible for making the resource
            available. Examples of a Publisher include a person, an
            organization, or a service. DCMI element.
:geo_location: (dict)

   :locality: (string) village, town, city or state
   :country: (string) Please use a standard two-letter country code
             defined by `ISO 3166-1 alpha-2
             <http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_. e.g. 'GB' or 'US'.
   :latitude: (number)
   :longitude: (number)

:rights_list: (list of dicts) License(s) under which this dataset is
              released.  Related to the 'rights' DCMI element.  
              Each element has these attributes:

   :uri: (string) License URI
   :name: (string) License name

:description_of_subjects: (string) A brief description of how subjects
                          were recruited.  Are they all PhD students,
                          for example?  Were they incentivised to
                          reduce their energy consumption?
:related_documents: (list of strings) References about this dataset
                    (e.g. references to academic papers or web pages).
                    Also briefly describe the contents of each
                    reference (e.g. does it contain a description of
                    the metering setup? Or an analysis of the data?)
                    Related to the 'relation' DCMI element.
:schema: (string) The URL of the NILM_metadata version (tag) against
         which this metadata is
         validated. e.g. https://github.com/nilmtk/nilm_metadata/tree/v0.2

.. _meter-device-schema:

MeterDevice
-----------

Metadata describing each model of electricity meter used in the
dataset.  (Please note that `ElecMeter`_ is used for representing
individual *instances* of meters in a building whilst ``MeterDevice`` is
used to represent information common to all instances of a specific
make and model of meter).

* Location in YAML: ``meter_devices.yaml``
* Location in HDF5: ``store.root._v_attrs.metadata`` in ``meter_devices``

One big dict.  Keys are device model names (e.g. 'EnviR').  The
purpose is to record information about specific models of meter.
Values are dicts with these keys:

:model: (string) (required) The model name for this meter device.
:model_url: (string) The URL with more information about this meter model.
:manufacturer: (string)
:manufacturer_url: (string)
:sample_period: (number) (required) The meter's nominal sample period
               (i.e. the length of time between consecutive
               samples) in seconds.
:max_sample_period: (number) (required) The maximum permissible length
                   of time between consecutive samples.  We assume the
                   meter is switched off during any gap longer than
                   ``max_sample_period``.
:measurements: (list) (required) The order is the order of the columns
  in the data table.

   :physical_quantity: (string) (required) One of {'power', 'energy',
                       'cumulative energy', 'voltage', 'current',
                       'state'}.  'state' columns store an integer
                       state ID where 0 is off and >0 refers to
                       defined states. (TODO: store mapping of state
                       ID per appliance to state name)
   :type: (string) (required for 'power' and 'energy') Alternative
           Current (AC) Type. One of {'reactive', 'active',
           'apparent'}.
   :upper_limit: (number)
   :lower_limit: (number)

:description: (string)
:wireless: (boolean)
:wireless_base: (string) Description of the base station used
:data_logger: (string) Description of the data logger used

.. _building-schema:

Building
--------

* Location in YAML: ``building<I>.yaml``
* Location in HDF5: ``store.root.building<I>._v_attrs.metadata``

:instance: (int) (required) The building instance in this dataset, starting from 1
:original_name: (string) Original name of building from old (pre-NILM
                Metadata) metadata.
:elec_meters: (dict of dicts) (required) Each key is an integer
              (>= 1) representing the meter instance in this building.
              Each value is an ``ElecMeter``. See section below on
              `ElecMeter`_.
:appliances: (list of dicts) (required) See section below on `Appliance`_.
:description: (string)
:rooms: (list of dicts):

   :name: (string) (required) one of {'lounge', 'kitchen', 'bedroom', 'utility',
                           'garage', 'basement', 'bathroom', 'study',
                           'nursery', 'hall', 'dining room',
                           'outdoors'}
   :instance: (int)
   :description: (string)
   :floor: (int) Ground floor is floor 0.
:n_occupants: (int) Mode number of occupants.
:temporal_coverage: (`Interval`_, see below)
:periods_unoccupied: (list of `Interval` objects, see below) Periods when this
                     building was empty for more than a day
                     (e.g. holidays)

Building metadata which is inherited from `Dataset`_ but can be
overridden by ``Building``:

* geo_location
* timezone
* temporal_coverage

.. _elec-meter-schema:

ElecMeter
---------

ElecMeters are the values of the ``elec_meters`` dict of each building (see the
section on `Building`_ metadata above).

:device_model: (string) (required) ``model`` which keys into ``meter_devices``
:submeter_of: (int) (required) the meter instance of the upstream meter.  Or 0
              to mean 'one of the site_meters'.
:submeter_of_is_uncertain: (boolean) Set to true if the value for
                           `submeter_of` is uncertain.
:upstream_meter_in_building: (int) If the upstream meter is
                             in a different building then specify that
                             building instance here.  If left blank
                             then we assume the upstream meter is in
                             the same building as this meter.
:site_meter: (boolean): required and set to True if this is a site
             meter (i.e. furthest upstream meter) otherwise not
             required.

.. _ElecMeter-room:

:room: (string) ``<room name>[,<instance>]``.  e.g. 'kitchen' or
       'bedroom,2'.  If no ``instance`` is specified (e.g. 'room:
       kitchen' then it is assumed to be 'kitchen,1'
       (i.e. kitchen instance 1).  If the building metadata specifies set of
       ``rooms`` then the room specified here will key into the
       building's ``rooms`` (but not all datasets enumerate every room
       for each building).
:floor: (int) Not necessary if ``room`` is specified. Ground floor is 0. 

:data_location: (string) (required) Path relative to root directory of
     dataset. e.g. ``house1/channel_2.dat``. Reference tables and
     columns within a Hierarchical file
     e.g. ``data.h5?table=/building1/elec/meter1`` or, if this
     metadata is stored in the same HDF file as the sensor data itself
     then just use the key e.g. ``/building1/elec/meter1``.

:preprocessing_applied: (dict): Each key is optional and is only
   present if that preprocessing function has been run.

   :clip: (dict)

      :lower_limit:
      :upper_limit:

:statistics: (dict):

   :good_sections: (list of `Interval`_ objects)
   :contiguous_sections: (list of `Interval`_ objects)
   :energy: (dict) kWh

      :active: (number)
      :reactive: (number)
      :apparent: (number)

.. _appliance-schema:

Appliance
---------

Each appliance dict has:

:type: (string) (required) appliance type (e.g. 'kettle'). Use NILM
       Metadata controlled vocabulary.  See
       `nilm_metadata/central_metadata/appliance_types/*.yaml <https://github.com/nilmtk/nilm_metadata/tree/master/central_metadata/appliance_types>`_.  Each ``*.yaml`` file in
       ``nilm_metadata/central_metadata/appliance_types`` is a large dictionary.  Each key
       in these dictionaries is a legal appliance ``type``.
:instance: (int starting from 1) (required) instance of this appliance within
           the building.
:meters: (list of ints) (required) meter instance(s) directly
        upstream of this appliance.  This is a list to handle the case
        where some appliances draw power from both 120 volt legs in a
        north American house.  Or 3-phase appliances.
:on_power_threshold: (number) watts
:minimum_off_duration: (number (seconds) in YAML; timedelta in HDF5)
:minimum_on_duration: (number (seconds) in YAML; timedelta in HDF5)
:dominant_appliance: (boolean) Is this appliance responsible for 
          most of the power demand on this meter?
:room: see `ElecMeter-room`_
:multiple: (boolean) True if there are more than one 
           of these appliances represented by this single
           ``appliance`` object.
           If there is exactly one appliance then do not specify
           ``multiple``.
:count: (int) If there are more than one of these appliances
        represented by this ``appliance`` object and if the exact
        number of appliances is known then specify that number here.
:control: (list of strings) Give a list of all control methods which
          apply.  For example, a video recorder would be both 'manual'
          and 'timer'.  The vocabulary is: {'timer', 'manual',
          'motion', 'sunlight', 'thermostat', 'always on'}
:efficiency_rating: (dict):

   :certification_name: (string) e.g. 'SEDBUK' or 'Energy Star 5.0'
   :rating: (string) e.g. 'A+'

:nominal_consumption: (dict):

   :on_power: (number) active power in watts when on.
   :standby_power: (number) active power in watts when in standby.
   :energy_per_year: (number) kWh per year
   :energy_per_cycle: (number) kWh per cycle

:components: (list of dicts): Components within this appliance. Each dict is an Appliance dict.
:model: (string)
:manufacturer: (string)
:original_name: (string)
:dates_active: (list of `Interval`_ objects, see below) Can be used to specify
               a change in appliance over time (for example if one
               appliance is replaced with another).
:year_of_purchase: (int) Four-digit year.
:year_of_manufacture: (int) Four-digit year.
:subtype: (string)
:part_number: (string)
:gtin: (int) http://en.wikipedia.org/wiki/Global_Trade_Item_Number
:version: (string)

Additional properties are specified for some Appliance Types.  Please
look up objects in
:file:`nilm_metadata/central_metadata/appliances/*.yaml` for details.

When an Appliance object is used as a component for an ApplianceType,
then the Appliance object may have :ref:`distributions-schema`
specified and may also use a property ``do_not_merge_categories:
true`` which prevents the system from merging categories from the
component into the container appliance.

.. _interval-schema:

Interval
---------

Represent an arbitrary time frame.  If either start or end is absent
then assume it equals the start or the end of the dataset,
respectively.  Please use `ISO 8601 format
<http://en.wikipedia.org/wiki/ISO_8601>`_ for dates or date times
(e.g. 2014-03-17 or 2014-03-17T21:00:52+00:00)

:start: (string)
:end: (string)
