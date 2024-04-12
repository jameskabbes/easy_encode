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


division = Division(1, set(
    [datetime_module.datetime.now(), datetime_module.datetime.now()]))

ee_client = client.Client()
ee_client.init_data_store('json', encoding_type_mappings={
                          datetime_module.datetime: type(None)})

print(division)
result = ee_client.encode_dataclass_object('json', division)
print(result)

# type_processing.test()
