class DataStoreNotSupported(Exception):

    MESSAGE = 'Data Store "{}" is not supported.'

    def __init__(self, data_store):
        super().__init__(DataStoreNotSupported.MESSAGE.format(data_store))
