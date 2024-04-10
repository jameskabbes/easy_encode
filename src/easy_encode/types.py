from typing import NewType, TypedDict, Any, Callable

ObjectAttribute = NewType('ObjectAttribute', str)
ObjectAttributeValue = NewType('ObjectAttributeValue', Any)
ObjectAttributeType = NewType('ObjectAttributeType', Any)
EncodingFunction = NewType(
    'EncodingFunction', Callable[[ObjectAttributeValue], Any])
DecodingFunction = NewType(
    'DecodingFunction', Callable[[ObjectAttributeValue], Any])

AttributeTypes = dict[ObjectAttribute, ObjectAttributeType]
AttributeEncodingFunctions = dict[ObjectAttribute, EncodingFunction]
AttributeDecodingFunctions = dict[ObjectAttribute, DecodingFunction]


class AttributeValueTypeConversion(TypedDict):
    encode: dict[ObjectAttributeType, AttributeEncodingFunctions]
    decode: dict[ObjectAttributeType, AttributeDecodingFunctions]


AttributeValueTypeConversions = dict[ObjectAttributeType,
                                     AttributeValueTypeConversion]

IsValueOfTypeFunction = Callable[[
    ObjectAttributeValue, ObjectAttributeType], bool]

IsValueOfTypeCollection = Callable[[
    Any, ObjectAttributeType, IsValueOfTypeFunction], bool]


class TypeCache(TypedDict):
    a: str


TypeCaches = dict[ObjectAttributeType, TypeCache]


class ClientConfig(TypedDict):
    cache_types: bool
    type_conversions_overwrite: AttributeValueTypeConversions
    type_conversions_additional: AttributeValueTypeConversions
