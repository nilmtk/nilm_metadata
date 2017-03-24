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
Dublin Core Metadata Initiative (DCMI)):

:name: (string) (required) Short name for the dataset.  e.g. 'REDD' or
       'UK-DALE'.  Equivalent DCMI element is 'title'.  If this
       dataset is the output of a disaggregation algorithm then `name`
       will be set to a short name for the algorithm; e.g. 'CO' or 'FHMM'.
:long_name: (string) Full name of the dataset, eg. 'Reference Energy
            Disaggregation Data Set'.
:creators: (list of strings) in the format '<Lastname>,
           <Firstname>'. DCMI element.
:timezone: (string) Please use the standard TZ name from the `IANA
           (aka Olson) Time Zone Database
           <http://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_ 
           e.g. 'America/New_York' or 'Europe/London'.
:date: (string) ISO 8601 format. e.g. '2014-06-23' Identical to the
       'date' DCMI element.
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
:timeframe: (`TimeFrame`_, see below) Start and end dates for
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
                          reduce their energy consumption?  How were
                          they chosen?
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

Metadata describing every model of meter used in the dataset.  (Please
note that `ElecMeter`_ is used for representing individual *instances*
of meters in a building whilst ``MeterDevice`` is used to represent
information common to all instances of a specific make and model of
meter).  Think of this section as a catalogue of meter models used in
the dataset.

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
                   ``max_sample_period``.  In other words, we define a
                   'gap' to be any two samples which are more than
                   ``max_sample_period`` apart.
:measurements: (list) (required) The order is the order of the columns
  in the data table.

   :physical_quantity: (string) (required) One of {'power', 'energy',
                       'cumulative energy', 'voltage', 'current',
                       'frequency', 'power factor', 'state', 'phase
                       angle', 'total harmonic distortion', 'temperature'}.  
                       'state' columns store an integer
                       state ID where 0 is off and >0 refers to
                       defined states. (TODO: store mapping of state
                       ID per appliance to state name).  Units: phase angle:
                       degrees; power: watts; energy: kWh; voltage:
                       volts; current: amps; temperature: degrees Celsius.
   :type: (string) (required for 'power' and 'energy') Alternative
           Current (AC) Type. One of {'reactive', 'active',
           'apparent'}.
   :upper_limit: (number)
   :lower_limit: (number)

:description: (string)
:pre_pay: (boolean) Is this a pre-pay meter?
:wireless: (boolean)

:wireless_configuration: (dict) All strings are human-readable free text:

   :base: (string) Description of the base station used. Manufacturer, model,
          version etc.
   :protocol: (string) e.g. 'zibgee', 'WiFi', 'custom'.  If
                    custom then add a link to documentation if
                    available.
   :carrier_frequency: (number) MHz
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
:water_meters: (dict of dicts) Same structure as ``elec_meters``.
:gas_meters: (dict of dicts) Same structure as ``elec_meters``.
:description: (string)
:rooms: (list of dicts):

   :name: (string) (required) one of {'lounge', 'kitchen', 'bedroom', 'utility',
                           'garage', 'basement', 'bathroom', 'study',
                           'nursery', 'hall', 'dining room',
                           'outdoors'}
   :instance: (int) (optional.  Starts from 1.  If absent then assume to be 1.)
   :description: (string)
   :floor: (int) Ground floor is floor 0.
:n_occupants: (int) Mode number of occupants.
:description_of_occupants: (string) free-text describing the
                           occupants.  Number of children, teenagers,
                           adults, pensioners?  Demographics?  Were
                           all occupants away from the house during
                           all week days?
:timeframe: (`TimeFrame`_, see below)
:periods_unoccupied: (list of `TimeFrame` objects, see below) Periods when this
                     building was empty for more than a day
                     (e.g. holidays)
:construction_year: (int) Four-digit calendar year of construction.
:energy_improvements: (list of strings) Any post-construction
                      modifications?  Some combination of
                      {'photovoltaics', 'solar thermal', 'cavity wall
                      insulation', 'loft insulation', 'solid wall
                      insulation', 'double glazing', 'secondary
                      glazing', 'triple glazing'}
:heating: (ordered list of strings, with the most dominant fuel first)
          Some combination of {'natural gas', 'electricity', 'coal',
          'wood', 'biomass', 'oil', 'LPG'}
:communal_boiler: boolean (set to true if heating is provided by a
                  shared boiler for the flats)
:ownership: (string) one of {'rented', 'bought'}
:building_type: (string) one of {'bungalow', 'cottage', 'detached',
                'end of terrace', 'flat', 'semi-detached',
                'mid-terrace', 'student halls', 'factory', 'office',
                'university'}

Building metadata which is inherited from `Dataset`_ but can be
overridden by ``Building``:

* geo_location
* timezone
* timeframe

.. _elec-meter-schema:

ElecMeter
---------

ElecMeters are the values of the ``elec_meters`` dict of each building (see the
section on `Building`_ metadata above).

:device_model: (string) (required) ``model`` which keys into ``meter_devices``
:submeter_of: (int) (required) the meter instance of the upstream
              meter.  Or set to ``0`` to mean "*one of the
              site_meters*".  In practice, ``0`` will be interpreted to
              mean "downstream of a 'MeterGroup' representing all the
              site meters summed together".
:submeter_of_is_uncertain: (boolean) Set to true if the value for
                           `submeter_of` is uncertain.
:upstream_meter_in_building: (int) If the upstream meter is
                             in a different building then specify that
                             building instance here.  If left blank
                             then we assume the upstream meter is in
                             the same building as this meter.
:site_meter: (boolean): required and set to True if this is a site
             meter (i.e. furthest upstream meter) otherwise not
             required.  If there are multiple mains phases
             (e.g. 3-phase mains) or multiple mains 'splits' (e.g. in
             North America where there are two 120 volt splits) then
             set ``site_meter=true`` in every site meter.  All
             non-site-meters directly downstream of the site meters
             should set ``submeter_of=0``.  Optionally also use
             ``phase`` to describe which phase this meter measures.
             What happens if there are multiple site meters in
             *parallel* (i.e. there are redundant meters)?  For
             example, perhaps there is a site meter installed by the
             utility company which provides infrequent readings; and
             there is also a fancy digital site meter which measures
             at the same point in the wiring tree and so, in a sense,
             the utility meter can be considered 'redundant' but is
             included in the dataset for comparison). In this
             situation, set ``site_meter=true`` in every site meter.
             Then set ``disabled=true`` in all but the 'favoured' site
             meter (which would usually be the site meter which
             provides the 'best' readings).  It is important to set
             ``disabled=true`` so NILMTK does not sum together
             parallel site meters.  The disabled site meters should
             also set ``submeter_of`` to the ID of the enabled site
             meter.  All non-site-meters directly downstream of site
             meters should set ``submeter_of=0``.
:utility_meter: (boolean) required and set to True if this is meter
                was installed by the utility company. Otherwise not
                required.
:timeframe: (`TimeFrame`_ object)
:name: (string) (optional) e.g. 'first floor total'.
:phase: (int or string) (optional) Used in multiple-phase setups.

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

:disabled: (bool): Set to true if NILMTK should ignore this channel.
           This is useful if, for example, this channel is a redundant 
           site_meter.

:preprocessing_applied: (dict): Each key is optional and is only
   present if that preprocessing function has been run.

   :clip: (dict)

      :lower_limit:
      :upper_limit:

:statistics: (list of dicts): Each dict describes statistics for
   one set of timeframes.  Each dict has:

   :timeframes: (list of `TimeFrame`_ objects) (required)  The timeframes
               over which these statistics were calculated.  If the
               stat(s) refer to the entire timeseries then enter the
               start and end of the timeseries as the only TimeFrame. 
   :good_sections: (list of `TimeFrame`_ objects)
   :contiguous_sections: (list of `TimeFrame`_ objects)
   :total_energy: (dict) kWh

      :active: (number)
      :reactive: (number)
      :apparent: (number)

   Note that some of these statistics are cached by 
   `NILMTK <http://nilmtk.github.io/>`_ at
   ``building<I>/elec/cache/meter<K>/<statistic_name>``. 
   For more details, see the docstring of 
   ``nilmtk.ElecMeter._get_stat_from_cache_or_compute()``.

WaterMeter and GasMeter
-----------------------

Same attributes as `ElecMeter`_.

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
:dominant_appliance: (boolean) (required if multiple appliances
                     attached to one meter). Is this appliance
                     responsible for most of the power demand on this
                     meter?
:on_power_threshold: (number) watts.  Not required.  Default is taken
                     from the appliance `type`.  The threshold (in
                     watts) used to decide if the appliance is `on` or `off`.
:max_power: (number) watts.  Not required.
:min_off_duration: (number) (seconds)  Not required.
:min_on_duration: (number) (seconds)  Not required.
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

:nominal_consumption: (dict):  Specifications reported by the manufacturer.

   :on_power: (number) active power in watts when on.
   :standby_power: (number) active power in watts when in standby.
   :energy_per_year: (number) kWh per year
   :energy_per_cycle: (number) kWh per cycle

:components: (list of dicts): Components within this appliance. Each dict is an Appliance dict.
:model: (string)
:manufacturer: (string)
:brand: (string)
:original_name: (string)
:model_url: (string) URL for this model of appliance
:manufacturer_url: (string) URL for the manufacturer
:dates_active: (list of `TimeFrame`_ objects, see below) Can be used to specify
               a change in appliance over time (for example if one
               appliance is replaced with another).
:year_of_purchase: (int) Four-digit year.
:year_of_manufacture: (int) Four-digit year.
:subtype: (string)
:part_number: (string)
:gtin: (int) http://en.wikipedia.org/wiki/Global_Trade_Item_Number
:version: (string)
:portable: (boolean)

Additional properties are specified for some Appliance Types.  Please
look up objects in
:file:`nilm_metadata/central_metadata/appliances/*.yaml` for details.

When an Appliance object is used as a component for an ApplianceType,
then the Appliance object may have a ``distributions`` dict (see
``ApplianceType:distributions`` in :doc:`central_metadata`)
specified and may also use a property ``do_not_merge_categories:
true`` which prevents the system from merging categories from the
component into the container appliance.

.. _timeframe-schema:

TimeFrame
---------

Represent an arbitrary time frame.  If either start or end is absent
then assume it equals the start or the end of the dataset,
respectively.  Please use `ISO 8601 format
<http://en.wikipedia.org/wiki/ISO_8601>`_ for dates or date times
(e.g. 2014-03-17 or 2014-03-17T21:00:52+00:00)

:start: (string)
:end: (string)
