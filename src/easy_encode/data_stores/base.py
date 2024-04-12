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
                encoded_values.append(cls._encode_value(obj, attribute, attribute_value, attribute_types[attribute])
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
    def _encode_value(cls, obj, attribute: ee_types.ObjectAttribute, attribute_value: ee_types.ObjectAttributeValue, attribute_type: ee_types.ObjectAttributeType) -> ee_types.ObjectAttributeValue:

        print('encoding value')

        # 1. find the actual type of value from nested type
        type_matches = type_processing.find_value_type_matches(
            attribute_value, attribute_type)

        print(attribute_value, attribute_type, type_matches)

        if len(type_matches) == 0:
            raise exceptions.AttributeValueTypeNotAsTyped(obj, attribute,
                                                          attribute_value, attribute_type)

        # 2. loop through type matches: start with most specific match, go to most general
        for type_match in type_matches[::-1]:

            print('type match: ', type_match)

            type_match_origin = typing.get_origin(type_match)

            # 2a. First, see if the type_match is a valid type of collection (tuple, list, dict, set, etc)
            if type_match_origin != None:
                nested_types = typing.get_args(type_match)
                encoded_type_origin = cls._get_desired_encoded_type(
                    type_match_origin)

                # see if this is a Mapping (dict) or Iterable (dict,list,set,tuple)
                is_mapping = False
                try:
                    is_mapping = issubclass(
                        encoded_type_origin, collections.abc.MutableMapping)
                except:
                    pass

                if is_mapping:
                    print('is mapping!')
                    encoded_mutable_mapping: collections.abc.MutableMapping = encoded_type_origin()
                    for key in attribute_value.keys():

                        # encode the value
                        if len(nested_types) > 1:
                            value = cls._encode_value(obj, attribute,
                                                      attribute_value.get(key), nested_types[1])
                        else:
                            value = attribute_value.get(key)

                        # encode the key
                        if len(nested_types) > 0:
                            key = cls._encode_value(obj, attribute,
                                                    key, nested_types[0])

                        encoded_mutable_mapping.__setitem__(key, value)
                    print('returned: ', encoded_mutable_mapping)
                    return encoded_mutable_mapping

                is_iterable = False
                try:
                    is_iterable = issubclass(
                        encoded_type_origin, collections.abc.Iterable)
                except:
                    pass

                if is_iterable:
                    print('is iterable!')
                    encoded_items = []
                    counter = 0
                    for item in iter(attribute_value):

                        print(item)
                        print(nested_types)

                        encoded_items.append(cls._encode_value(obj, attribute,
                                                               item, nested_types[min(counter, len(nested_types)-1)] if len(nested_types) > 0 else ...))
                        counter += 1

                    encoded_iterable = encoded_type_origin(encoded_items)
                    print('returned: ', encoded_iterable)
                    return encoded_iterable

            encoded_type = cls._get_desired_encoded_type(type_match)

            # see what to convert the item to
            if type_match in data_conversions.TYPE_CONVERSIONS:
                if 'encode' in data_conversions.TYPE_CONVERSIONS[type_match]:
                    if encoded_type in data_conversions.TYPE_CONVERSIONS[type_match]['encode']:
                        encoding_function = data_conversions.TYPE_CONVERSIONS[
                            type_match]['encode'][encoded_type]
                        encoded_value = encoding_function(attribute_value)
                        print('returning encoding function map: ', encoded_value)
                        return encoded_value

        # outside of loop for type_matches
        print('returning original attribute_value: ', attribute_value)
        return attribute_value
