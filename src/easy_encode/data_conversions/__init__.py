import datetime
from easy_encode.data_conversions import datetime as datetime_conversions
from easy_encode import types

TYPE_CONVERSIONS: types.AttributeValueTypeConversions = {

    datetime.datetime: {
        'encode': {
            int: lambda x: int(datetime_conversions.datetime_to_float(x)),
            float: lambda x: datetime_conversions.datetime_to_float(x),
            str: lambda x: datetime_conversions.datetime_to_str(x)
        },
        'decode': {
            int: lambda x: datetime_conversions.datetime_from_number(x),
            float: lambda x: datetime_conversions.datetime_from_number(x),
            str: lambda x: datetime_conversions.datetime_from_str(x)
        }
    },
}
