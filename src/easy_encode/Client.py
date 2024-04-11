from easy_encode import types as ee_types, data_stores, types as ee_types
import typing


class Client:

    types: dict

    def __init__(self, config: ee_types.ClientConfig = {}):
        pass

    def encode_dataclass_object(self,
                                data_store: data_stores.DATA_STORES,
                                obj,
                                encoding_functions: ee_types.AttributeEncodingFunctions = {}
                                ):

        attribute_types = obj.__annotations__
        return self.encode_object(data_store, obj, attribute_types, encoding_functions)

    def encode_object(self, data_store: data_stores.DATA_STORES, obj, attribute_types: ee_types.AttributeTypes, encoding_functions: ee_types.AttributeEncodingFunctions = {}):

        data_store_class = data_stores.get_data_store(data_store)
        return data_store_class._encode_object(obj, attribute_types, encoding_functions)
