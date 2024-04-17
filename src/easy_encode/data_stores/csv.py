from easy_encode.data_stores.base import DataStore as BaseDataStore
from easy_encode.types import ObjectAttributeValue


class DataStore(BaseDataStore):
    DATA_STORE = 'csv'
    ENCODE_RETURN_TYPE = str
