from easy_encode.data_stores.base import DataStore as BaseDataStore
import datetime
import json


class DataStore(BaseDataStore):
    DATA_STORE = 'json'
    DEFAULT_ENCODING_TYPE_MAPPINGS = {
        set: list,
        datetime.datetime: str,
    }
