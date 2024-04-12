from easy_encode import client, type_processing, types as ee_types
from dataclasses import dataclass, field
import typing
import datetime as datetime_module

IDTyp = typing.NewType('IDTyp', typing.Union[typing.Union[int, None], str])
IDType = typing.NewType('IDType', IDTyp)
DivisionID = IDType

a = typing.NewType('a', set[datetime_module.datetime])


@dataclass
class Division:
    id: DivisionID
    datetimes: a
    test: list[list[dict[int, str]]]


division = Division(1, set(
    [datetime_module.datetime.now(), datetime_module.datetime.now()]), [[{1: '1'}]])

ee_client = client.Client()
print(division)
result = ee_client.encode_dataclass_object('json', division)
print(result)

# type_processing.test()
