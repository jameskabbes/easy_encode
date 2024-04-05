from typing import NewType, TypedDict, Any, Callable

ObjectAttribute = NewType('ObjectAttribute', str)
ObjectAttributeValue = NewType('ObjectAttributeValue', Any)
ObjectAttributeType = NewType('ObjectAttributeType', Any)
EncodingFunction = NewType('EncodingFunction', Callable)
DecodingFunction = NewType('DecodingFunction', Callable)

AttributeTypes = dict[ObjectAttribute, ObjectAttributeType]
AttributeEncodingFunctions = dict[ObjectAttribute, EncodingFunction]
AttributeDecodingFunctions = dict[ObjectAttribute, DecodingFunction]
