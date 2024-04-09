from collections.abc import Mapping
from typing import NewType, TypedDict, Any, Callable

a: Mapping

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
    encode: dict[Any, Callable]
    decode: dict[Any, Callable]


AttributeValueTypeConversions = dict[ObjectAttributeType,
                                     AttributeValueTypeConversion]
