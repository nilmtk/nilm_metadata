**********************************
NILM Metadata
**********************************

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
not use inheritance for all subtypes?  The rule of thumb is that is a
subtype is functionally different to its parent then it should be
specified as a separate object (for example, a gas hob and an electric
hob clearly have radically different electricity usage profiles) but
if the differences are minor (e.g. a digital radio versus an analogue
radio) then these should be specified as subtypes of the same object.

Naming conventions
------------------

* properties are lowercase with underscores, e.g. `main_room_light`
* object names (not specific makes and models) are lowercase with
  spaces, unless they are acronyms in which case they are uppercase
  (e.g. 'LED')
* object names of specific makes and models are uppercase with a tilde
  to separate the manufacturer from the model e.g. `Samsung~RSU1R`
