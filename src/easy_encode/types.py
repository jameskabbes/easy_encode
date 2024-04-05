from typing import NewType, TypedDict, Any, Callable

ObjectAttribute = NewType('ObjectAttribute', str)
type AttributesAndTypes = dict[ObjectAttribute, list[type]]
type EncodingFunction = Callable


class TypeConversion(TypedDict):
    encode: dict[type, Callable]
    decode: dict[type, Callable]


type TypeConversions = dict[type, TypeConversion]
