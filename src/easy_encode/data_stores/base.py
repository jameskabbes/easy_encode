import typing
from easy_encode import types, data_conversions, type_processing, exceptions


class DataStore:

    DATA_STORE: str
    ENCODE_RETURN_TYPE: typing.Any
    ENCODING_TYPE_MAPPING: dict[types.ObjectAttributeType,
                                types.ObjectAttributeType]

    @classmethod
    def _encode_object(cls, obj, attribute_types: dict[types.ObjectAttribute, types.ObjectAttributeType], attribute_encoding_functions: types.AttributeDecodingFunctions = {}) -> tuple:
        """encode an object with a given set of attribute types and encoding functions, returns a list of encoded values"""

        encoded_values = []
        for attribute in attribute_types:
            encoded_values.append(cls._encode_value(obj, attribute,
                                                    getattr(obj, attribute), attribute_types[attribute], None if attribute not in attribute_encoding_functions else attribute_encoding_functions[
                                                        attribute])
                                  )
        return tuple(encoded_values)

    @classmethod
    def _encode_value(cls, obj, attribute: types.ObjectAttribute, attribute_value: types.ObjectAttributeValue, attribute_type: types.ObjectAttributeType, encoding_function: types.EncodingFunction | None):
        """recursively encode nested values"""

        print()
        print(attribute)
        print(attribute_value)
        print(attribute_type)

        # 1. encoding function takes precendent
        if encoding_function != None:
            return encoding_function(attribute_value)

        # 2. find the actual type of value from nested type
        found_match, actual_type = type_processing.find_first_match(
            attribute_value, attribute_type)

        if not found_match:
            raise exceptions.AttributeValueTypeNotAsTyped(obj, attribute,
                                                          attribute_value, attribute_type)

        print('actual_type')
        print(actual_type)

        # 3. find desired type
        for encoding_type in cls.ENCODING_TYPE_MAPPING:

            # is set[datetime] a type of set, or list[int] a type of list
            if type_processing.is_type_of_type(actual_type, encoding_type):
                wanted_type = cls.ENCODING_TYPE_MAPPING[actual_type]

                print('wanted_type')
                print(wanted_type)

                if actual_type in data_conversions.TYPE_CONVERSIONS:
                    if 'encode' in data_conversions.TYPE_CONVERSIONS[actual_type]:
                        if wanted_type in data_conversions.TYPE_CONVERSIONS[actual_type]['encode']:
                            encoding_function = data_conversions.TYPE_CONVERSIONS[
                                actual_type]['encode'][wanted_type]

                            return encoding_function(attribute_value)

        return attribute_value

        """

        while True:

            # see if we are mapping this to anything
            if attribute_type in cls.ENCODING_TYPE_MAPPING:
                mapped_type = cls.ENCODING_TYPE_MAPPING[attribute_type]

            # 3. check if we have a union type - extract which one it is
            attribute_type_origin = typing.get_origin(attribute_type)
            attribute_type_args = typing.get_args(attribute_type)

            # we have a union of multiple types - select which type it actually is
            if attribute_type_origin == None and len(attribute_type_args) > 1:
                for attribute_type_arg in attribute_type_args:
                    if type_processing.is_value_of_type(attribute_value, attribute_type_arg):
                        attribute_type = attribute_type_arg
                        break

            # 4. find the supertype of attribute type
            attribute_supertype = type_processing.find_supertype(
                attribute_type)

            # 5. Check out the
            if attribute_supertype in cls.ENCODING_TYPE_MAPPING:
                cast_function = cls.ENCODING_TYPE_MAPPING[attribute_supertype]

                # cast it to the new type / call function
                return cast_function(attribute_value)

            if type(attribute_type) == typing.NewType:
                attribute_type: typing.NewType = attribute_type.__supertype__
            else:
                return attribute_value

        """
