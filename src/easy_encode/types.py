from typing import NewType, TypedDict, Any, Callable

ObjectAttribute = NewType('ObjectAttribute', str)
type AttributesAndTypes = dict[ObjectAttribute, list[type]]
type EncodingFunction = Callable
