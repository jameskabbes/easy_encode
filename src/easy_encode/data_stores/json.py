from easy_encode.data_stores.base import DataStore as BaseDataStore
import datetime
import json


class DataStore(BaseDataStore):
    DATA_STORE = 'json'
    ENCODE_RETURN_TYPE = str

    ENCODING_TYPE_MAPPING = {
        set: list,
        datetime.datetime: str
    }
