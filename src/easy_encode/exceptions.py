from easy_encode import types


class DataStoreNotSupported(Exception):

    MESSAGE = 'Data Store "{}" is not supported.'

    def __init__(self, data_store):
        super().__init__(DataStoreNotSupported.MESSAGE.format(data_store))


class AttributeValueTypeNotAsTyped(Exception):

    MESSAGE = 'Object {} given attribute "{}" value of {} is not of type {}'

    def __init__(self, obj, att, attribute_value: types.ObjectAttributeValue, attribute_type: types.ObjectAttributeType):
        super().__init__(AttributeValueTypeNotAsTyped.MESSAGE.format(type(obj), att,
                                                                     attribute_value, attribute_type))
