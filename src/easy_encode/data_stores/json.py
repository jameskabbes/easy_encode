from easy_encode.data_stores.base import DataStore as BaseDataStore
import json


class DataStore(BaseDataStore):
    DATA_STORE = 'json'
    ENCODE_RETURN_TYPE = str
