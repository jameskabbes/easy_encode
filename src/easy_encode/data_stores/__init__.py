from typing import Literal, TypedDict, Any
from easy_encode.data_stores import base, csv, json, sqlite, text
from easy_encode import exceptions

type DATA_STORES = Literal['json', 'sqlite', 'text', 'csv']


DATA_STORE_MODULES: dict[DATA_STORES, base.DataStore] = {
    'json': json.DataStore,
    'csv': csv.DataStore,
    'sqlite': sqlite.DataStore,
    'text': text.DataStore
}


def get_data_store(data_store: DATA_STORES):

    if data_store not in DATA_STORE_MODULES:
        raise exceptions.DataStoreNotSupported(data_store)
    else:
        return DATA_STORE_MODULES[data_store]
