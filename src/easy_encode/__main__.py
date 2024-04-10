from easy_encode import client, type_processing
from dataclasses import dataclass, field
import typing
import datetime as datetime_module

IDTyp = typing.NewType('IDTyp', typing.Union[typing.Union[int, None], str])
IDType = typing.NewType('IDType', IDTyp)
DivisionID = IDType


@dataclass
class Division:
    id: DivisionID
    datetime: typing.Optional[datetime_module.datetime]
    datetimes: set[datetime_module.datetime]


division = Division(1, datetime_module.datetime.now(), set(
    [datetime_module.datetime.now()]))

easy_encode_client = client.Client()
result = easy_encode_client.encode_dataclass_object(division, 'json')

print(result)
