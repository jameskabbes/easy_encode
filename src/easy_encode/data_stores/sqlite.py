from easy_encode.data_stores.base import DataStore as BaseDataStore


class DataStore(BaseDataStore):
    DATA_STORE = 'sqlite'
    ENCODE_RETURN_TYPE = None
