from easy_encode import types as ee_types, data_stores, types as ee_types


class Client:

    types: dict

    def __init__(self, config: ee_types.ClientConfig = {}):
        pass

    def encode_dataclass_object(self,
                                obj,  # is a dataclass
                                data_store: data_stores.DATA_STORES,
                                attribute_types: ee_types.AttributeTypes | None = None,
                                attribute_encoding_functions: ee_types.AttributeEncodingFunctions | None = None
                                ):

        data_store_class = data_stores.get_data_store(data_store)
        if attribute_types == None:
            attribute_types = obj.__annotations__
        if attribute_encoding_functions == None:
            attribute_encoding_functions = {}

        return data_store_class._encode_object(obj, attribute_types, attribute_encoding_functions)
