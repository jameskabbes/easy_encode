from easy_encode.data_stores.base import DataStore as BaseDataStore
import datetime


class DataStore(BaseDataStore):
    DATA_STORE = 'sqlite'
    ENCODE_RETURN_TYPE = None

    ENCODING_TYPE_MAPPING = {
        bool: int,
        datetime.datetime: str
    }
