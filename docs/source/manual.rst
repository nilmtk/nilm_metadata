********************
NILM Metadata Manual
********************

Before reading this manual, please make sure you have read the NILM
Metadata `README <https://github.com/nilmtk/nilm_metadata/blob/master/README.md>`_
which introduces the project.  Also, if you are not
familiar with YAML, please see the 
`WikiPedia page on YAML <http://en.wikipedia.org/wiki/YAML>`_ 
for a quick introduction.

NILM Metadata allows us to describe many of the objects we typically
find in a disaggregated energy dataset.  Below is a UML Class Diagram
showing all the classes and the relationships between classes:

.. image:: schema.svg

A dark black diamond indicates a 'composition' relationship whilst a
hollow diamond indicates an 'aggregation'. For example, the
relationship between ``Dataset`` and ``Building`` is read as '*each
Dataset contains any number of Buildings and each Building belongs to
exactly one Dataset*'. We use hollow diamonds to mean that objects of
one class *refer* to objects in another class. For example, each
``Appliance`` object refers to exactly one
``ApplianceType``. Instances of the classes in the shaded area on the
left are intended to be shipped with each dataset whilst objects of
the classes on the right are common to all datasets and are stored
within the NILM Metadata project. Some ``ApplianceTypes`` contain
``Appliances``, hence the box representing the ``Appliance`` class
slightly protrudes into the ‘common metadata’ area on the right.

Below we will use examples to illustrate how to build a metadata
schema for a dataset.

Examples
========

Simple example
--------------

The illustration below shows a cartoon mains wiring diagram for
a domestic building. Black lines indicate mains wires. This home has a
split-phase mains supply (common in North America, for example). The
washing machine draws power across both splits. All other appliances
draw power from a single split.

.. image:: circuit_no_metadata.svg

The text below shows a minimalistic description (using the NILM
Metadata schema) of the wiring diagram above.  The YAML below
would go into the file ``building1.yaml``.

.. highlight:: yaml
::

  instance: 1 # this is the first building in the dataset
  elec_meters: # a dictionary where each key is a meter instance
    1:
      site_meter: true # meter 1 measures the whole-building aggregate
    2:
      site_meter: true
    3:
      submeter_of: 1 # meter 3 is directly downstream of meter 1
    4:
      submeter_of: 1
    5:
      submeter_of: 2
    6:
      submeter_of: 2
    7:
      submeter_of: 6
  appliances:
  - {type: kettle, instance: 1, room: kitchen, meters: [3]}
  - {type: washing machine, instance: 1, meters: [4,5]}
  - {type: light, instance: 1, room: kitchen, meters: [7]}
  - {type: light, instance: 2, multiple: true, meters: [6]}

``elec_meters`` holds a dictionary of dictionaries.  Each key is a
meter instance (a unique integer identifier within the building).  We
start numbering from 1 because that is common in existing datasets.
Each value of the ``elec_meters`` dict is a dictionary recording
information about that specific meter. ``site_meter`` is set to
``true`` if this meter measures the whole-building aggregate power
demand. ``submeter_of`` records the meter instance of the upstream
meter.  In this way, we can specify wiring hierarchies of arbitrary
complexity.

``appliances`` is a list of dictionaries.  Each dictionary describes a
single appliance.  The appliance ``type`` (e.g. 'kettle' or 'washing
machine') is taken from a controlled vocabulary defined in NILM
Metadata.  For each appliance, we must also specify an ``instance``
(an integer which, within each building, allows us to distinguish
between multiple instances of a particular appliance ``type``).  We
must also specify a list of ``meters``.  Each element in this list is
an integer which corresponds to a meter ``instance``.  In this way, we
can specify which meter is directly upstream of this appliance.  The
vast majority of domestic appliances will only specify a single meter.
We use two meters for north-American appliances which draw power from
both mains legs.  We use three meters for three-phase appliances.

See the documentation of the :doc:`dataset_metadata` for a full
listing of all elements which can be described, or continue below for
a more detailed example.


Detailed example of converting REDD to NILM Metadata
----------------------------------------------------
