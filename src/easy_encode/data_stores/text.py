from easy_encode.data_stores.base import DataStore as BaseDataStore


class DataStore(BaseDataStore):
    DATA_STORE = 'text'
    ENCODE_RETURN_TYPE = str
