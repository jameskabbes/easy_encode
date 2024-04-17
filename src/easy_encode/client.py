from easy_encode import types as ee_types, types as ee_types, exceptions, data_conversions, type_processing, data_stores as ee_data_stores
import typing
import collections.abc


class Client:

    data_stores: dict[ee_data_stores.DATA_STORES,
                      ee_data_stores.base.DataStore]
    type_conversions: ee_types.AttributeValueTypeConversions
    encoding_type_mappings: ee_types.EncodingTypeMappings

    def __init__(self, type_conversions: ee_types.AttributeValueTypeConversions = {}, encoding_type_mappings: ee_types.EncodingTypeMappings = {}):
        self.data_stores = {}
        self.type_conversions = type_conversions
        self.encoding_type_mappings = encoding_type_mappings

    def init_data_store(self, data_store: ee_data_stores.DATA_STORES, type_conversions: ee_types.AttributeValueTypeConversions = {}, encoding_type_mappings: ee_types.EncodingTypeMappings = {}):
        self.data_stores[data_store] = ee_data_stores.get_data_store(
            data_store)(type_conversions=type_conversions, encoding_type_mappings=encoding_type_mappings)

    def encode_dataclass_object(self, data_store: ee_data_stores.DATA_STORES, obj, encoding_functions: ee_types.EncodingFunctions = {}):
        attribute_types = obj.__annotations__
        return self.encode_object(data_store, obj, attribute_types, encoding_functions)

    def encode_object(self, data_store: ee_data_stores.DATA_STORES, obj, attribute_types: ee_types.AttributeTypes, encoding_functions: ee_types.EncodingFunctions = {}):

        encoded_values = self._encode_values(
            data_store, obj, attribute_types, encoding_functions)
        return self.data_stores[data_store]._postprocess_encoded_object(encoded_values, obj, attribute_types)

    def encode_objects(self, data_store: ee_data_stores.DATA_STORES, objs: collections.abc.Iterable, attribute_types: ee_types.AttributeTypes, encoding_functions: ee_types.EncodingFunctions = {}) -> tuple[tuple]:
        """include a series of objects"""

        encoded_tuples = [self.encode_object(
            data_store, obj, attribute_types, encoding_functions) for obj in objs]
        return tuple(encoded_tuples)

    def _get_encoding_function(self, data_store: ee_data_stores.DATA_STORES, attribute_type: ee_types.ObjectAttributeType, encoded_type: ee_types.ObjectAttributeType) -> ee_types.EncodingFunction | None:
        return self._get_conversion_function(data_store, 'encode', attribute_type, encoded_type)

    def _get_decoding_function(self, data_store: ee_data_stores.DATA_STORES, attribute_type: ee_types.ObjectAttributeType, encoded_type: ee_types.ObjectAttributeType) -> ee_types.DecodingFunction | None:
        return self._get_conversion_function(data_store, 'decode', attribute_type, encoded_type)

    def _get_conversion_function(self, data_store: ee_data_stores.DATA_STORES, conversion_type: ee_types.ConversionFunctionType, attribute_type: ee_types.ObjectAttributeType, encoded_type: ee_types.ObjectAttributeType) -> ee_types.ConversionFunctionBase | None:

        def find(type_conversions: ee_types.AttributeValueTypeConversions, conversion_type: ee_types.ConversionFunctionType, attribute_type: ee_types.ObjectAttributeType, encoded_type: ee_types.ObjectAttributeType):
            if attribute_type in type_conversions:
                if conversion_type in type_conversions[attribute_type]:
                    if encoded_type in type_conversions[attribute_type][conversion_type]:
                        return type_conversions[attribute_type][conversion_type][encoded_type]
                    elif 'default' in type_conversions[attribute_type][conversion_type]:
                        return type_conversions[attribute_type][conversion_type]['default']
            return None

        for type_conversions in [self.data_stores[data_store].type_conversions, self.data_stores[data_store].DEFAULT_TYPE_CONVERSIONS, self.type_conversions, data_conversions.TYPE_CONVERSIONS]:
            conversion_function = find(
                type_conversions, conversion_type, attribute_type, encoded_type)
            if conversion_function != None:
                return conversion_function
        return None

    def _get_encoding_type_mapping(self, data_store: ee_data_stores.DATA_STORES, attribute_type: ee_types.ObjectAttributeType) -> ee_types.ObjectAttributeType | None:
        """find which encoding type mapping is relevant for a given attribute type"""

        if attribute_type in self.data_stores[data_store].encoding_type_mappings:
            return self.data_stores[data_store].encoding_type_mappings[attribute_type]
        if attribute_type in self.data_stores[data_store].DEFAULT_ENCODING_TYPE_MAPPINGS:
            return self.data_stores[data_store].DEFAULT_ENCODING_TYPE_MAPPINGS[attribute_type]
        if attribute_type in self.encoding_type_mappings:
            return self.encoding_type_mappings[attribute_type]

        return None

    def _encode_values(self, data_store: ee_data_stores.DATA_STORES, obj, attribute_types: ee_types.AttributeTypes, encoding_functions: ee_types.EncodingFunctions = {}) -> tuple[ee_types.ObjectAttributeValue]:

        if data_store not in self.data_stores:
            self.init_data_store(data_store)

        encoded_values = []
        for attribute in attribute_types:
            attribute_value: ee_types.ObjectAttributeValue = getattr(
                obj, attribute)

            # encoding function takes full precedent
            if attribute in encoding_functions:
                encoded_value = encoding_functions[attribute](attribute_value)

            else:
                encoding_function = self._get_encoding_function(
                    data_store, attribute, encoding_functions)
                if encoding_function != None:
                    encoded_value = encoding_functions[attribute](
                        attribute_value)

                else:
                    encoded_value = self._encode_value(data_store,
                                                       obj, attribute, attribute_value, attribute_types[attribute])

            encoded_values.append(encoded_value)

        return tuple(encoded_values)

    def _encode_value(self, data_store: ee_data_stores.DATA_STORES, obj, attribute: ee_types.ObjectAttribute, attribute_value: ee_types.ObjectAttributeValue, attribute_type: ee_types.ObjectAttributeType) -> ee_types.ObjectAttributeValue:
        """encode the attribute value of a certain object and type"""

        # 1. find the actual type of value from nested type
        type_matches = type_processing.find_value_type_matches(
            attribute_value, attribute_type)

        if len(type_matches) == 0:
            raise exceptions.AttributeValueTypeNotAsTyped(obj, attribute,
                                                          attribute_value, attribute_type)

        # 2. loop through type matches: start with most specific match, go to most general
        for type_match in type_matches[::-1]:

            type_match_origin = typing.get_origin(type_match)

            # 2a. First, see if the type_match is a valid type of collection (tuple, list, dict, set, etc)
            if type_match_origin != None:
                nested_types = typing.get_args(type_match)

                encoded_type_origin = type_match_origin

                encoded_type_origin = self._get_encoding_type_mapping(data_store,
                                                                      type_match_origin)

                if encoded_type_origin == None:
                    encoded_type_origin = type_match_origin

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
                            value = self._encode_value(data_store, obj, attribute,
                                                       attribute_value.get(key), nested_types[1])
                        else:
                            value = attribute_value.get(key)

                        # encode the key
                        if len(nested_types) > 0:
                            key = self._encode_value(data_store, obj, attribute,
                                                     key, nested_types[0])

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

                        encoded_items.append(self._encode_value(data_store, obj, attribute,
                                                                item, nested_types[min(counter, len(nested_types)-1)] if len(nested_types) > 0 else ...))
                        counter += 1

                    encoded_iterable = encoded_type_origin(encoded_items)
                    return encoded_iterable

            mapped_type = self._get_encoding_type_mapping(
                data_store, type_match)
            if mapped_type == None:
                mapped_type = type_match

            # see what to convert the item to
            encoding_function = self._get_encoding_function(
                data_store, type_match, mapped_type)

            if encoding_function != None:
                encoded_value = encoding_function(attribute_value)
                return encoded_value

        # outside of loop for type_matches
        return attribute_value
