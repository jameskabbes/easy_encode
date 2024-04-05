from typing import Any, Self, Callable
from easy_encode import types, data_conversions


class DataStore:

    DATA_STORE: str
    TYPE_CONVERSIONS: types.TypeConversions = {}
    ENCODE_RETURN_TYPE: Any

    @classmethod
    def encode_object(cls, obj: Any, attributes_and_types: types.AttributesAndTypes, attribute_encoding_functions: dict[types.ObjectAttribute, types.EncodingFunction] = {}):
        pass

    @classmethod
    def encode_object_attribute(cls, value: Any, encoding_function: types.EncodingFunction | None = None):

        # 1. specified encoding function for value
        if encoding_function != None:
            return encoding_function(value)

        # get the root type of the value
        value_type = type(value)

        # 2. data store specific encoding function
        if value_type in cls.TYPE_CONVERSIONS:
            if 'encode' in cls.TYPE_CONVERSIONS[value_type]:
                return cls.TYPE_CONVERSIONS['encode'][value_type](value)

        # 3. default encoding function for value type
        if value_type in data_conversions.TYPE_CONVERSIONS:
            if 'encode' in data_conversions.TYPE_CONVERSIONS[value_type]:
                return cls.TYPE_CONVERSIONS['encode'][value_type](value)
