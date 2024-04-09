import typing
from easy_encode import types, data_conversions, type_processing


class DataStore:

    DATA_STORE: str
    TYPE_CONVERSIONS: str
    ENCODE_RETURN_TYPE: typing.Any
    ENCODING_TYPE_MAPPING: dict[types.ObjectAttributeType,
                                types.ObjectAttributeType]

    @classmethod
    def _encode_object(cls, obj, attribute_types: dict[types.ObjectAttribute, types.ObjectAttributeType], attribute_encoding_functions: types.AttributeDecodingFunctions = {}) -> tuple:
        """encode an object with a given set of attribute types and encoding functions, returns a list of encoded values"""

        encoded_values = (cls._encode_value(
            getattr(obj, attribute), attribute_types[attribute], None if attribute not in attribute_encoding_functions else attribute_encoding_functions[
                attribute]) for attribute in attribute_types)

        return encoded_values

    @classmethod
    def _encode_value(cls, attribute_value: types.ObjectAttributeValue, attribute_type: types.ObjectAttributeType, encoding_function: types.EncodingFunction | None):
        """recursively encode nested values"""

        # 1. encoding function takes precendent
        if encoding_function != None:
            return encoding_function(attribute_value)

        while True:

            used_type = type_processing.which_type_is_value(
                attribute_value, attribute_type)

            pass

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
