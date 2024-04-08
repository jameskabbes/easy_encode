import typing
from easy_encode import types, data_conversions, type_processing


class DataStore:

    DATA_STORE: str
    TYPE_CONVERSIONS: str
    ENCODE_RETURN_TYPE: typing.Any
    ENCODING_TYPE_MAPPING: dict[types.ObjectAttributeType, typing.Any]

    @classmethod
    def _encode_object(cls, obj, attribute_types: dict[types.ObjectAttribute, types.ObjectAttributeType], attribute_encoding_functions: types.AttributeDecodingFunctions) -> list:
        """encode an object with a given set of attribute types and encoding functions, returns a list of encoded values"""

        encoded_values = []
        for attribute in attribute_types:
            attribute_encoding_function = None if attribute not in attribute_encoding_functions else attribute_encoding_functions[
                attribute]

            encoded_value = cls._encode_value(
                getattr(obj, attribute), attribute_types[attribute], attribute_encoding_function)

            encoded_values.append(encoded_value)
        return encoded_values

    @classmethod
    def _encode_value(cls, attribute_value: types.ObjectAttributeValue, attribute_type: types.ObjectAttributeType, encoding_function: types.EncodingFunction | None = None):

        # 1. specified encoding function for value
        if encoding_function != None:
            return encoding_function(attribute_value)

        # 2. find the supertype of attribute type
        attribute_supertype = type_processing.find_supertype(attribute_type)

        if len(typing.get_args(attribute_supertype)) > 1:

            # what to do we when have multiple types?
            print('we have multiple types here')
            return attribute_value

        if attribute_type in cls.ENCODING_TYPE_MAPPING:
            new_attribute_type = cls.ENCODING_TYPE_MAPPING[attribute_type]
            print(attribute_type, new_attribute_type)

            # try casting it to the new type
            return new_attribute_type(attribute_value)

        return attribute_value
