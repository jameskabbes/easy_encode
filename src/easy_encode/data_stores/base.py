from typing import Any, Self, Callable
from easy_encode import types, data_conversions, type_processing


class DataStore:

    DATA_STORE: str
    TYPE_CONVERSIONS: str
    ENCODE_RETURN_TYPE: Any
    ENCODING_TYPE_MAPPING: dict[types.ObjectAttributeType, Any]

    @classmethod
    def _encode_object(cls, obj, attributes: list[types.ObjectAttribute], attribute_encoding_functions: types.AttributeDecodingFunctions) -> list:

        encoded_values = []
        for attribute in attributes:
            attribute_value: types.ObjectAttributeValue = getattr(
                obj, attribute)

            attribute_encoding_function = None if attribute not in attribute_encoding_functions else attribute_encoding_functions[
                attribute]

            encoded_value = cls._encode_value(
                attribute_value, attribute_encoding_function)

            encoded_values.append(encoded_value)
        return encoded_values

    @classmethod
    def _encode_value(cls, attribute_value: types.ObjectAttributeValue, encoding_function: types.EncodingFunction | None = None):

        # 1. specified encoding function for value
        if encoding_function != None:
            return encoding_function(attribute_value)

        # 2. find the type of the attribute value, map it
        attribute_type = type(attribute_value)

        if attribute_type in cls.ENCODING_TYPE_MAPPING:
            new_attribute_type = cls.ENCODING_TYPE_MAPPING[attribute_type]
            print(attribute_type, new_attribute_type)

            # try casting it to the new type
            return new_attribute_type(attribute_value)

        return attribute_value
