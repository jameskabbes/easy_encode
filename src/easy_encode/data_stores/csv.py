from easy_encode.data_stores.base import DataStore as BaseDataStore
from easy_encode import types as ee_types


class DataStore(BaseDataStore):
    DATA_STORE = 'csv'
    ENCODE_RETURN_TYPE = str
    DEFAULT_ENCODING_TYPE = str

    DEFAULT_ENCODING_TYPE_MAPPINGS = {
        set: set,
        list: list,
        tuple: tuple,
        dict: dict
    }

    @classmethod
    def _postprocess_encoded_objects(cls, encoded_nested_values: tuple[tuple[ee_types.ObjectAttributeValue]], attribute_types: dict[ee_types.ObjectAttribute, ee_types.ObjectAttributeType]) -> str:

        print(encoded_nested_values)

        return '\n'.join(','.join(attribute_type for attribute_type in attribute_types), '\n'.join(','.join(item) for item in encoded_nested_values))
