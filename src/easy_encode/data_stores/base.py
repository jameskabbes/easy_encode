import typing
from easy_encode import types as ee_types, data_conversions, type_processing, exceptions
import collections.abc

import datetime


class DataStore:

    DATA_STORE: str
    ENCODE_RETURN_TYPE: typing.Any
    ENCODING_TYPE_MAPPING: dict[ee_types.ObjectAttributeType,
                                ee_types.ObjectAttributeType]

    @classmethod
    def _encode_object(cls, obj, attribute_types: ee_types.AttributeTypes, encoding_functions: ee_types.AttributeEncodingFunctions = {}) -> tuple:
        """encode an object with a given set of attribute types and encoding functions, returns a tuple of encoded values"""

        encoded_values = []
        for attribute in attribute_types:
            attribute_value: ee_types.ObjectAttributeValue = getattr(
                obj, attribute)

            # encoding function takes full precedent
            if attribute in encoding_functions:
                encoded_values.append(
                    encoding_functions[attribute](attribute_value))

            else:
                encoded_values.append(cls._encode_value(attribute_value, attribute_types[attribute])
                                      )

        return tuple(encoded_values)

    @classmethod
    def _get_desired_encoded_type(cls, actual_type: ee_types.ObjectAttributeType) -> ee_types.ObjectAttributeType:

        if actual_type in cls.ENCODING_TYPE_MAPPING:
            return cls.ENCODING_TYPE_MAPPING[actual_type]

        if type(actual_type) == typing.NewType:
            return cls._get_desired_encoded_type(actual_type.__supertype__)
        return actual_type

    @classmethod
    def _encode_value(cls, attribute_value: ee_types.ObjectAttributeValue, attribute_type: ee_types.ObjectAttributeType, encoded_type: ee_types.ObjectAttributeType | None = None) -> ee_types.ObjectAttributeValue:

        print('encoding value')

        # 1. find the actual type of value from nested type
        found_match, actual_type = type_processing.is_value_of_type(
            attribute_value, attribute_type)

        print('got it')
        print(attribute_value, attribute_type, actual_type)

        if not found_match:
            raise exceptions.AttributeValueTypeNotAsTyped(
                attribute_value, attribute_type)

        # 3. see if we have special nested values in collections to deal with
        actual_type_origin = typing.get_origin(actual_type)

        if actual_type_origin != None:
            nested_types = typing.get_args(actual_type)

            encoded_type_origin = cls._get_desired_encoded_type(
                actual_type_origin)

            print('actual type origin')
            print(actual_type_origin)
            print('encoded type origin')
            print(encoded_type_origin)

            # see if this is a Mapping (dict) or Iterable (dict,list,set,tuple)
            is_mapping = False
            try:
                is_mapping = issubclass(
                    encoded_type_origin, collections.abc.MutableMapping)
            except:
                pass

            if is_mapping:
                encoded_mutable_mapping: collections.abc.MutableMapping = encoded_type_origin()
                for key in attribute_value.keys():

                    # encode the value
                    if len(nested_types) > 1:
                        value = cls._encode_value(
                            attribute_value.get(key), nested_types[1])
                    else:
                        value = attribute_value.get(key)

                    # encode the key
                    if len(nested_types) > 0:
                        key = cls._encode_value(key, nested_types[0])

                    encoded_mutable_mapping.__setitem__(key, value)
                return encoded_mutable_mapping

            is_iterable = False
            try:
                is_iterable = issubclass(
                    encoded_type_origin, collections.abc.Iterable)
            except:
                pass

            if is_iterable:
                encoded_items = []
                counter = 0
                for item in iter(attribute_value):

                    encoded_items.append(cls._encode_value(
                        item, nested_types[min(counter, len(nested_types)-1)] if len(nested_types) > 0 else ...))
                    counter += 1

                a = encoded_type_origin(encoded_items)
                print('a')
                print(a)

                return a

        encoded_type = cls._get_desired_encoded_type(actual_type)

        # see what to convert the item to
        if actual_type in data_conversions.TYPE_CONVERSIONS:
            if 'encode' in data_conversions.TYPE_CONVERSIONS[actual_type]:
                if encoded_type in data_conversions.TYPE_CONVERSIONS[actual_type]['encode']:
                    encoding_function = data_conversions.TYPE_CONVERSIONS[
                        actual_type]['encode'][encoded_type]
                    return encoding_function(attribute_value)

        return attribute_value
