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
