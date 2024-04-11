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
    datetimes: set[datetime_module.datetime]


division = Division(1, list(
    [datetime_module.datetime.now(), datetime_module.datetime.now()]))

easy_encode_client = client.Client()
print(division)
result = easy_encode_client.encode_dataclass_object('json', division)
print(result)

# type_processing.test()
