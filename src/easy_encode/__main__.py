from easy_encode import client, type_processing, types as ee_types, data_stores
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
    test: list[dict[int, int]]


division = Division(1, set(
    [datetime_module.datetime.now(), datetime_module.datetime.now()]), [{1: 2}, {3: 4}])

ee_client = client.Client()
ee_client.init_data_store('csv')

print(division)
result = ee_client.encode_objects(
    'csv', [division, division], Division.__annotations__)
print(result)


# type_processing.test()
