from typing import NewType, TypedDict, Any, Callable, Required, Literal

ObjectAttribute = NewType('ObjectAttribute', str)
ObjectAttributeValue = NewType('ObjectAttributeValue', Any)
ObjectAttributeType = NewType('ObjectAttributeType', Any)
type AttributeTypes = dict[ObjectAttribute, ObjectAttributeType]

type ConversionFunctionBase = Callable[[
    ObjectAttributeValue], ObjectAttributeValue]
type ConversionFunctionType = Literal['encode', 'decode']

type EncodingFunction = ConversionFunctionBase
type DecodingFunction = ConversionFunctionBase

type ConversionFunctions[T] = dict[ObjectAttribute, T]
type EncodingFunctions = ConversionFunctions[EncodingFunction]
type DecodingFunctions = ConversionFunctions[DecodingFunction]

EncodingTypeMappings = dict[ObjectAttributeType, ObjectAttributeType]


type AttributeValueTypeConversions = dict[ObjectAttributeType,
                                          dict[ConversionFunctionType, dict[ObjectAttributeType |
                                                                            Literal['default'], ConversionFunctionBase]]]
