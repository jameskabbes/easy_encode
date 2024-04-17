from easy_encode.data_stores.base import DataStore as BaseDataStore
from easy_encode import types as ee_types
import datetime
import json


class DataStore(BaseDataStore):
    DATA_STORE = 'json'
    DEFAULT_ENCODING_TYPE_MAPPINGS = {
        set: list,
        datetime.datetime: str,
    }

    @classmethod
    def _postprocess_encoded_object(cls, encoded_values: tuple[ee_types.ObjectAttributeValue], attribute_types: ee_types.AttributeTypes) -> str:
        attributes = list(attribute_types.keys())
        return json.dumps({attributes[i]: encoded_values[i] for i in range(len(encoded_values))})
