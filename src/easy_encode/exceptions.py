from easy_encode import types as ee_types


class DataStoreNotSupported(Exception):

    MESSAGE = 'Data Store "{}" is not supported.'

    def __init__(self, data_store):
        super().__init__(DataStoreNotSupported.MESSAGE.format(data_store))


class AttributeValueTypeNotAsTyped(Exception):

    MESSAGE = 'Object {} attribute "{}" value of {} is not as typed {}'

    def __init__(self, obj, attribute: ee_types.ObjectAttribute, attribute_value: ee_types.ObjectAttributeValue, attribute_type: ee_types.ObjectAttributeType):
        super().__init__(AttributeValueTypeNotAsTyped.MESSAGE.format(obj, attribute,
                                                                     attribute_value, attribute_type))
