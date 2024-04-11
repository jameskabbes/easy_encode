from easy_encode import types


class DataStoreNotSupported(Exception):

    MESSAGE = 'Data Store "{}" is not supported.'

    def __init__(self, data_store):
        super().__init__(DataStoreNotSupported.MESSAGE.format(data_store))


class AttributeValueTypeNotAsTyped(Exception):

    MESSAGE = 'value of {} is not of type {}'

    def __init__(self, attribute_value: types.ObjectAttributeValue, attribute_type: types.ObjectAttributeType):
        super().__init__(AttributeValueTypeNotAsTyped.MESSAGE.format(
            attribute_value, attribute_type))
