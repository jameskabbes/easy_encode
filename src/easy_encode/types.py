from typing import NewType, TypedDict, Any, Callable, Required

ObjectAttribute = NewType('ObjectAttribute', str)
ObjectAttributeValue = NewType('ObjectAttributeValue', Any)
ObjectAttributeType = NewType('ObjectAttributeType', Any)
EncodingFunction = NewType(
    'EncodingFunction', Callable[[ObjectAttributeValue], ObjectAttributeValue])
DecodingFunction = NewType(
    'DecodingFunction', Callable[[ObjectAttributeValue], ObjectAttributeValue])

AttributeTypes = dict[ObjectAttribute, ObjectAttributeType]
AttributeEncodingFunctions = dict[ObjectAttribute, EncodingFunction]
AttributeDecodingFunctions = dict[ObjectAttribute, DecodingFunction]


class AttributeValueTypeConversion(TypedDict):
    encode: dict[ObjectAttributeType, AttributeEncodingFunctions]
    decode: dict[ObjectAttributeType, AttributeDecodingFunctions]


AttributeValueTypeConversions = dict[ObjectAttributeType,
                                     AttributeValueTypeConversion]


class TypeCache(TypedDict):
    a: str


TypeCaches = dict[ObjectAttributeType, TypeCache]


class ClientConfig(TypedDict):
    cache_types: bool
    type_conversions_overwrite: AttributeValueTypeConversions
    type_conversions_additional: AttributeValueTypeConversions


class IsValueOfTypeFunctionKwargs(TypedDict):
    allow_union: bool
    allow_subclass: bool
    allow_any: bool
