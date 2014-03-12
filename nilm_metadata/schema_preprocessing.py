from __future__ import print_function, division
from jsonschema import RefResolver, Draft4Validator
from file_management import get_schema_directory


def get_local_resolver(schema):
    # based on sblask's answer here:
    # https://github.com/Julian/jsonschema/issues/98#issuecomment-17531405
    schema.pop('id', None)
    return RefResolver('file://'+get_schema_directory()+'/', schema)


def combine(schema):
    """A solution to the problem that if we use 'allOf' in a schema
    then we cannot enforce 'additionalProperties=False'.
    `Combine` finds instances of 'allOf' and combines the properties
    into the main schema's properties, and also sets additionalProperties=False
    and resolves references locally.
    """

    # based on Julian's answer here:
    # https://github.com/Julian/jsonschema/issues/150#issuecomment-36457164
    properties = schema.setdefault("properties", {})
    resolver = get_local_resolver(schema)
    subschemas = [schema]
    while subschemas:
        subschema = subschemas.pop()
        ref = subschema.pop("$ref", None)
        if ref:
            with resolver.resolving(ref) as r:
                subschema = r
        properties.update(subschema.get("properties", {}))
        subschemas.extend(subschema.pop("allOf", ()))

    schema["additionalProperties"] = False

    
def local_validate(instance, schema):
    """Like jsonschema.validate except we use the local
    filesystem to resolve references, not the network.
    """
    resolver = get_local_resolver(schema)
    Draft4Validator(schema, resolver=resolver).validate(instance)
