from easy_encode import encode_dataclass_object
from dataclasses import dataclass, field
from typing import Set, NewType, TypedDict, Callable, Any, Union, Literal
import datetime

IDTyp = NewType('IDTyp', Union[Union[int, None], str])
IDType = NewType('IDType', IDTyp)
DivisionID = IDType


@dataclass
class Division:
    id: DivisionID
    datetime: datetime.datetime
    numbers: set[set[dict[str, int]]]
    name: Union[str, None] = field(default=None)


division = Division(1, datetime.datetime.now(), set([1, 2, 3, 4]), 'east')
print(encode_dataclass_object(division, 'json'))
