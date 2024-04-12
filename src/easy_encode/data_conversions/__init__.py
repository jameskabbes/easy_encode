import datetime
from easy_encode.data_conversions import datetime_conversions as datetime_conversions
from easy_encode import types as ee_types

TYPE_CONVERSIONS: ee_types.AttributeValueTypeConversions = {

    datetime.datetime: {
        'encode': {
            'default': lambda x: datetime_conversions.datetime_to_str(x),
            int: lambda x: int(datetime_conversions.datetime_to_float(x)),
            float: lambda x: datetime_conversions.datetime_to_float(x),
            str: lambda x: datetime_conversions.datetime_to_str(x),
        },
        'decode': {
            int: lambda x: datetime_conversions.datetime_from_number(x),
            float: lambda x: datetime_conversions.datetime_from_number(x),
            str: lambda x: datetime_conversions.datetime_from_str(x)
        }
    },
}
