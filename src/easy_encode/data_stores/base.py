from easy_encode import types as ee_types


class DataStore:

    DATA_STORE: str
    DEFAULT_ENCODING_TYPE_MAPPINGS: ee_types.EncodingTypeMappings = {}
    encoding_type_mappings: ee_types.EncodingTypeMappings

    DEFAULT_TYPE_CONVERSIONS: ee_types.AttributeValueTypeConversions = {}
    type_conversions: ee_types.AttributeValueTypeConversions

    def __init__(self, type_conversions: ee_types.AttributeValueTypeConversions = {}, encoding_type_mappings: ee_types.EncodingTypeMappings = {}):
        self.type_conversions = type_conversions
        self.encoding_type_mappings = encoding_type_mappings

    @classmethod
    def _postprocess_encoded_object(cls, encoded_values: tuple[ee_types.ObjectAttributeValue], attribute_types: ee_types.AttributeTypes):
        return encoded_values

    @classmethod
    def _postprocess_encoded_objects(cls, encoded_nested_values: tuple[tuple[ee_types.ObjectAttributeValue]], attribute_types: ee_types.AttributeTypes):

        postprocessed = [cls._postprocess_encoded_object(
            encoded_nested_values[i], attribute_types) for i in range(len(encoded_nested_values))]

        return tuple(postprocessed)
