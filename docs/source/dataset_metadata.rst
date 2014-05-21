****************
Dataset metadata
****************

This page describes the metadata schema for describing a dataset.

There are two file formats for the metadata: YAML and HDF5.  
YAML metadata files should be in a ``metadata`` folder.
Each section of this doc starts by describing where the relevant
metadata is stored in both file formats.


Dataset
-------

* Location in YAML: ``dataset.yaml``
* Location in HDF5: ``store.root._v_attrs.metadata``

Metadata attributes (some of these attributes are adapted from the
Dublin Core Metadata Initiative or DCMI):

:name: (string) (required) Short name for the dataset.  e.g. 'REDD' or
       'UK-DALE'.  Equivalent DCMI element is 'title'.
:long_name: (string) Full name of the dataset, eg. 'Reference Energy
            Disaggregation Data Set'.
:mains_voltage: (dict):

   :nominal: (number) (required) volts
   :upper_limit: (number) volts
   :lower_limit: (number) volts

:identifier: (string): A digital object identifier (DOI) or URI for
             the dataset.  DCMI element.
:subject: (string): For example, is this dataset about domestic or
          commercial buildings?  Does it include disaggregated
          appliance-by-appliance data or just whole-building data?
          DCMI element.  Human-readable free text.
:geospatial_coverage: (string): Spatial coverage.  e.g. 'Southern
                      England'. Related to the 'coverage' DCMI
                      element.
:temporal_coverage: (`TimeFrame`_, see below)
:creators: (list of strings) in the format '<Lastname>,
           <Firstname>'. DCMI element.
:funding: (list of strings) A list of all the sources of funding used
          to produce this dataset.
:publisher: (string) The entity responsible for making the resource
            available. Examples of a Publisher include a person, an
            organization, or a service. DCMI element.
:geo_location: (dict)

   :locality: (string) village, town or city
   :country: (string) Please use a standard two-letter country code
             defined by `ISO 3166-1 alpha-2
             <http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_. e.g. 'GB' or 'US'.
   :latitude: (number)
   :longitude: (number)

:timezone: (string) Please use the standard TZ name from the `IANA
           (aka Olson) Time Zone Database
           <http://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_ 
           e.g. 'America/New_York' or 'Europe/London'.
:timeframe: (`TimeFrame`_, see below)
:publication_date: (string) Related to the 'date' DCMI element.
:rights_list: (list of dicts) License(s) under which this dataset is released.  Related to the 'rights' DCMI element.  Each element has these attributes:

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
                    the metering setup? Or an analysis of the data?
                    Related to the 'relation' DCMI element.
:contact: (string) Email address
:institution: (string)
:description: (string) DCMI element
:number_of_buildings: (int)
:schema: (string) The URL of the NILM_metadata version (tag) against
         which this metadata is
         validated. e.g. https://github.com/nilmtk/nilm_metadata/tree/v0.2.0


MeterDevice
-----------

Metadata describing each model of electricity meter used in the
dataset.  (Please note that `ElecMeter`_ is used for representing
individual *instances* of meters in a building whilst MeterDevice is
used to represent information common to all instances of a specific
make and model of meter).

* Location in YAML: ``meter_devices.yaml``
* Location in HDF5: ``store.root._v_attrs.metadata`` in ``meter_devices``

One big dict.  Keys are device model names (e.g. 'EnviR').  The
  purpose is to record information about specific models of meter.
  Values are also dicts with keys:

:model: (string) (required) The model name for this meter device.
:model_url: (string) The URL with more information about this meter model.
:manufacturer: (string)
:manufacturer_url: (string)
:sample_period: (number) (required) The meter's sample period
               (i.e. the length of time between consecutive
               samples) in seconds.
:max_sample_period: (number) The maximum permissible length of time
                   between consecutive samples.  We assume the
                   meter is switched off during any gap longer
                   than ``max_sample_period``.
:measurements: (list of dicts) The order is the order of the columns
               in the data table: 

   :physical_quantity: (string) (required) One of {'power', 'energy',
                       'voltage'}
   :ac_type: (string) (required) Alternative Current (AC) Type. One
             of {'reactive', 'active', 'apparent'}
   :upper_limit: (number)
   :lower_limit: (number)
:description: (string)
:wireless: (boolean)
:wireless_base: (string) Description of the base station used
:data_logger: (string) Description of the data logger used


Building
--------

* Location in YAML: ``building<I>.yaml``
* Location in HDF5: ``store.root.building<I>._v_attrs.metadata``

:instance: (int) (required) The building instance in this dataset, starting from 1
:dataset: (string) (required) Dataset ``name``
:original_name: (string) Original name of building from old (pre-NILM
                Metadata) metadata.
:elec_meters: (list of dicts) (required) See section below on `Meter metadata`_.
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
:temporal_coverage: (`TimeFrame`_, see below)
:periods_unoccupied: (list of `TimeFrame` objects, see below) Periods when this
                     building was empty for more than a day
                     (e.g. holidays)


Building metadata which is inherited from `Dataset`_ but can be
overridden by ``Building``:

* geo_location
* timezone
* timeframe


ElecMeter
---------

This lives in the ``elec_meters`` attribute of each building (see the
section on `Building`_ metadata above).

:device_model: (string) (required) ``model`` which keys into ``meter_devices``
:instance: (int starting from 1) (required) the meter instance within the building.
:submeter_of: (int) (required) the meter instance of the upstream meter.  Or 0
              to mean 'one of the site_meters'.
:submeter_of_is_uncertain: (boolean) Set to true if the value for
                           `submeter_of` is uncertain.
:upstream_meter_in_building: (int) Only use if the upstream meter is
                             in a different building.  If left blank
                             then we assume the upstream meter is in
                             the same building as this meter.
:site_meter: (boolean): True if this is a site meter (i.e. furthest
             upstream meter)
:preprocessing: (list of dicts):

   :filter: (string) one of {'clip', ... TODO}  If ``filter==clip``
            then use these additional attributes: ``lower_limit, upper_limit``.

:room: (dict) with ``name`` [and ``instance``].
:floor: (int)
:category: (string) e.g. ``lighting`` or ``sockets``.  Use this if this meter
           feeds a group of appliances and if we do not know the
           identity of each individual appliance.  For example, perhaps
           this is a meter which measures the lighting circuit,
           in which case we use ``'category': 'lighting'``.
           Must use NILM Metadata controlled vocabulary as for
           appliance categories.
:appliances: (list of dicts) See section below on `Appliance metadata`_.
:sensors: (list of dicts) Some homes have a split-phase mains
           supply. Some homes have 3-phase mains.  Some
           appliances take two or three supplies.  All these
           situations are handled by specifying the location
           of data for one or more sensors.  Each dict includes:
   :data_location: (string) Path relative to root directory of
                   dataset. e.g. 'house1/channel_2.dat'. Reference
                   tables and columns within a Hierarchical
                   file e.g. 'data.h5?table=/building1/sensor1a' or, if
                   this metadata is stored in the same HDF file as the
                   sensor data itself then just use the key e.g. '/building1/sensor1a'.


We can also store the results from stats functions:

:good_sections: (list of `TimeFrame`_ objects)
:contiguous_sections: (list of `TimeFrame`_ objects)
:energy: (dict) kWh

   :active: (number)
   :reactive: (number)
   :apparent: (number)



Appliance metadata
------------------

Each appliance dict has:

:type: (string) (required) appliance type. Use NILM Metadata controlled
       vocabulary.  See ``nilm_metadata/objects/*.yaml``.  Legal
       appliance names are the keys in these files.
:instance: (int starting from 1) (required) instance of this appliance within
           the building.
:on_power_threshold: (number) watts
:minimum_off_duration: (number in YAML; timedelta in HDF5)
:minimum_on_duration: (number in YAML; timedelta in HDF5)
:dominant_appliance: (boolean) Is this appliance responsible for 
          most of the power demand on this meter?
:room: (dict) with ``name`` [and ``instance``]
:count: (int) number of appliance instances.  If absent then assumed
        to be 1.
:multiple: (boolean) True if there are more than one but an unknown
           number of these appliances.  If there are more than one
           appliance and the exact number is known then use ``count``.
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

:components: (list of dicts): Each dict is an Appliance dict.
:model: (string)
:manufacturer: (string)
:original_name: (string)
:dates_active: (list of `TimeFrame`_ objects, see below) Can be used to specify
               a change in appliance over time (for example if one
               appliance is replaced with another).
:year_of_purchase: (int)
:year_of_manufacture: (int)
:subtype: (string)
:part_number: (string)
:gtin: (int) http://en.wikipedia.org/wiki/Global_Trade_Item_Number
:version: (string)

Additional properties are specified for some Appliance Types.  Please
look up objects in `objects/*.yaml` for details.

TimeFrame
---------

Represent an arbitrary time frame.  If either start or end is absent
then assume it equals the start or the end of the dataset,
respectively.  Please use `ISO 8601 format
<http://en.wikipedia.org/wiki/ISO_8601>`_ for dates or date times
(e.g. 2014-03-17 or 2014-03-17T21:00:52+00:00)

:start: (string)
:end: (string)
