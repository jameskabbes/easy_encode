from typing import Any, Self, Callable
from easy_encode import types


class DataStore:

    DATA_STORE: str
    ENCODE_CONVERSIONS: dict = {}
    DECODE_CONVERSIONS: dict = {}
    ENCODE_RETURN_TYPE: Any

    @classmethod
    def encode_object(cls, obj: Any, attributes_and_types: types.AttributesAndTypes, attribute_encoding_functions: dict[types.ObjectAttribute, types.EncodingFunction] = {}):
        pass

    @classmethod
    def encode_object_attribute(cls, value: Any, encoding_function: types.EncodingFunction | None = None):
        pass
