from easy_encode import encode_dataclass_object, type_processing
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
    numbers: set[int]
    numbers2: set[float]
    name: Union[str, None] = field(default=None)


"""
division = Division(1, datetime.datetime.now(), set(
    [1, 2, 3, 4]), set([1.0, 2.0]), 'east')
print(encode_dataclass_object(division, 'json'))
"""

type_processing.test()
