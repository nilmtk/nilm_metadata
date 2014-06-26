.. highlight:: yaml

**********************************
Central appliance metadata
**********************************

Manual
======

Common info about appliances is stored in NILM Metadata.  This includes:

* Categories for each appliance type
* prior knowledge about the distribution of variables such as:

  * on power
  * on duration
  * usage in terms of hour per day
  * appliance correlations (e.g. that the TV is usually on if the games console is on)
* valid additional properties for each appliance
* mapping from country codes to nominal mains voltage ranges

The central info about appliances uses a simple but powerful
inheritance mechanism to allow appliances to inherit from a other
appliances.  For example, 'laptop computer' is a specialisation of
'computer' and the two share several properties (e.g. both are in the
'ICT' category).  So 'laptop computer' inherits from 'computer' and
modifies and adds any properties it needs.  In this way, we can
embrace the
`don't repeat yourself (DRY) <http://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_
principal by exploiting the relationship between appliances.


Inheritance
-----------

* protypical inheritance; like JavaScript
* dicts are updated; lists are extended; other properties are overwritten
* arbitrary inheritance depth

Components
----------

* recursive
* categories of appliance is updated with categories from each component

Subtypes versus a new child object
----------------------------------

Appliance specification objects can take a 'subtype' property.  Why
not use inheritance for all subtypes?  The rule of thumb is that if a
subtype is functionally different to its parent then it should be
specified as a separate o child bject (for example, a gas hob and an electric
hob clearly have radically different electricity usage profiles) but
if the differences are minor (e.g. a digital radio versus an analogue
radio) then the appliances should be specified as subtypes of the same object.

Naming conventions
------------------

* properties are lowercase with underscores, e.g. `main_room_light`
* object names (not specific makes and models) are lowercase with
  spaces, unless they are acronyms in which case they are uppercase
  (e.g. 'LED')
* object names of specific makes and models are uppercase with a tilde
  to separate the manufacturer from the model e.g. `Samsung~RSU1R`
* category names are lowercase with spaces
* ambersands are replaced with 'and'

Categories
----------

:Traditional: wet, cold, consumer electronics, ICT, cooking, heating
:Misc: misc, sockets
:Size: small, large
:Electrical: 
  - lighting, incandescent, fluorescent, compact, linear, LED
  - resistive
  - power electronics
  - SMPS, no PFC, passive PFC, active PFC
  - single-phase induction motor, capacitor start-run, constant torque


Example
-------

To demonstrate the inheritance system, let's look at specifying a
boiler.

First, NILM Metadata specifies a 'heating appliance' object, which is
can be considered the 'base class'::

  heating appliance:
    parent: appliance
    categories:
      traditional: heating
      size: large

Next, we specify a 'boiler' object, which inherits from 'heating appliance'::


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


Finally, in the metadata for the dataset itself, we can do::

  type: boiler
  manufacturer: Worcester
  model: Greenstar 30CDi Conventional natural gas
  room: bathroom
  year_of_purchase: 2011
  fuel: natural gas
  subtype: regular
  part_number: 41-311-71
  efficiency_rating: 
    certification_name: SEDBUK
    rating: A
  nominal_consumption:
    on_power: 70


Schema details
==============

Below is a UML Class Diagram
showing all the classes and the relationships between classes:

.. image:: schema.svg

(Please see the :doc:`manual` for more background about the NILM
Metadata schema)

Below we describe all the classes and their attributes and possible values.

ApplianceType
-------------

Has many of the attributes that :ref:`appliance-schema` has, with the addition
of:

:distributions: (dict) Distribution of random variables.

   :on_power: (array of priors, see below) bin_edges in units of watts
   :on_duration: (array of priors, see below) bin_edges in units of seconds
   :off_duration: (array of priors, see below) bin_edges in units of seconds
   :usage_hour_per_day: (array of priors, see below) bin_edges = [0,1,2,...,24]
   :usage_day_per_week: (array of priors, see below) categories =
                        ['mon', 'tue', ..., 'sun']
   :usage_month_per_year: (array of priors, see below) bin_edges are
                          in units of days (we need bin edges because
                          months are not equal lengths).  The first
                          bin represents January.
   :rooms: (array of priors, see below) Categorical distribution over
           the rooms where this appliance is likely to be
           used. e.g. for a fridge this might be 'kitchen:0.9,
           garage:0.1'.  Please use the standard room names defined in
           room.json (category names in distributions are not
           automatically validated).
   :subtypes: (array of priors, see below) Categorical distribution
              over the subtypes.
   :appliance_correlations: (array of priors, see below) list of other
                            appliances. Probability of this appliance
                            being on given that the other appliance is
                            on. e.g. 'tv:0.1, amp:0.4, ...' means that
                            there is a 10% probability of this
                            appliance being on if the TV is on.  Each
                            category name can either be just an
                            appliance name (e.g. 'fridge') or
                            <appliance name>,<appliance instance>
                            e.g. 'fridge,1'
   :ownership_per_country: (array of priors, see below) Probability of
                           this appliance being owned by a household
                           in each country (i.e. a categorical
                           distribution where categories are standard
                           two-letter country code defined by ISO
                           3166-1 alpha-2. e.g. 'GB' or 'US'.
                           http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). If
                           the probability refers to the entire globe
                           then use 'GLOBAL' as the country code.
   :ownership_per_continent: (array of priors, see below) Probability
                             of this appliance being owned by a
                             household in each country (i.e. a
                             categorical distribution where categories
                             are standard two-letter continent code
                             defined at
                             http://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_continent_%28data_file%29

Country
-------

One large dict specifying country-specific information.

Each key is a 'country' (string). Please use a
standard two-letter country code defined by `ISO 3166-1 alpha-2
<http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>`_. e.g. 'GB' or
'US'.

Each value is a dict with the following attributes:

:mains_voltage: (dict):

   :nominal: (number) (required) volts
   :upper_limit: (number) volts
   :lower_limit: (number) volts


Priors
------

TODO.  For now, please see /schema/prior.json
