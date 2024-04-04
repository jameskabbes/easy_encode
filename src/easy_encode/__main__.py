from typing import Union
from dataclasses import dataclass, field
import datetime as datetime_module
from easy_encode.data_stores import get_data_store


@dataclass
class Datetime:
    id: int
    start_datetime: Union[datetime_module.datetime, None] = field(
        default=datetime_module.datetime.max)


dt = Datetime(1, datetime_module.datetime.now())
print('Python Object: ')
print(dt)
print(str(dt))

get_data_store('asdfasdf')
