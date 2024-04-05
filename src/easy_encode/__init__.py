from easy_encode import types, data_stores


def encode_dataclass_object(
    obj,  # is a dataclass
    data_store: data_stores.DATA_STORES,
    attribute_types: types.AttributeTypes | None = None,
    attribute_encoding_functions: types.AttributeEncodingFunctions | None = None
):

    data_store_class = data_stores.get_data_store(data_store)
    if attribute_types == None:
        attribute_types = obj.__annotations__
    if attribute_encoding_functions == None:
        attribute_encoding_functions = {}

    return data_store_class._encode_object(obj, attribute_types, attribute_encoding_functions)
