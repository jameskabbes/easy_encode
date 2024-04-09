from easy_encode import types
import typing
import collections.abc


def find_supertype(given_type):
    """go up the chain of given_type NewType definitions until we reach the base"""

    while type(given_type) == typing.NewType:
        given_type = given_type.__supertype__
    return given_type


def is_value_of_type_mapping(value: collections.abc.Mapping, given_type: types.ObjectAttributeType) -> bool:
    """recursively check if the first key-value pair of Mapping object is of given_type"""

    nested_types = typing.get_args(given_type)
    for key in value.keys():

        # check key
        if len(nested_types) < 1:
            break
        if not is_value_of_type(key, nested_types[0]):
            return False

        # check value
        if len(nested_types) < 2:
            break
        if not is_value_of_type(value[key], nested_types[1]):
            return False

    return True


def is_value_of_type_iterable(value: typing.Iterable, given_type: types.ObjectAttributeType) -> bool:
    nested_types = typing.get_args(given_type)

    counter = 0
    for item in iter(value):
        if counter >= len(nested_types):
            break
        if not is_value_of_type(item, nested_types[counter]):
            return False

        counter += 1

    return True


NESTED_TYPE_CHECKING: dict[type, typing.Callable[[typing.Any, typing.Any], bool]] = {
    collections.abc.Mapping: is_value_of_type_mapping,
    collections.abc.Iterable: is_value_of_type_iterable,
}


def which_type_is_value(value: types.ObjectAttributeValue, given_type: types.ObjectAttributeType) -> types.ObjectAttributeType:

    given_type_args = typing.get_args(given_type)
    given_type_origin = typing.get_origin(given_type)

    pass


def is_value_of_type(value: types.ObjectAttributeValue, given_type: types.ObjectAttributeType) -> bool:
    """recursively check if value is of type: given_type"""

    print(value, given_type)
    value_type = type(value)
    print(value_type)

    # strip down the user defined NewTypes
    given_supertype = find_supertype(given_type)
    print('supertype')
    print(given_supertype)

    # see if this is a Mapping (dict) or Iterable (dict,list,set,tuple)
    given_supertype_origin = typing.get_origin(given_supertype)
    print('origin')
    print(given_supertype_origin)
    if given_supertype_origin != None:
        for nested_type in (collections.abc.Mapping, collections.abc.Iterable):
            if issubclass(given_supertype_origin, nested_type):
                return NESTED_TYPE_CHECKING[nested_type](value, given_type)

    # not a nested type
    given_supertype_args = typing.get_args(given_supertype)
    print('args')
    print(given_supertype_args)

    # union type
    if len(given_supertype_args) > 1:
        for given_supertype_arg in given_supertype_args:
            if is_value_of_type(value, given_supertype_arg):
                return True
        return False
    else:
        return value_type == given_supertype or given_type == ...


def find_priority_type(given_type):
    """for types that are a Union of other types, return the first one"""

    given_type_args = typing.get_args(given_type)
    if len(given_type_args) > 1:
        given_type = given_type_args[0]
    return given_type


def find_origin_type(given_type):
    """reduce things like list[int] to list"""

    given_type_origin = typing.get_origin(given_type)
    if given_type_origin != None:
        given_type = given_type_origin
    return given_type


def find_root_type(given_type):

    # a. find supertype
    given_type = find_supertype(given_type)

    # b. find priority type
    given_type = find_priority_type(given_type)

    # c. find origin type
    given_type = find_origin_type(given_type)

    return given_type


def test():
    """
    print(is_value_of_type(True, bool))
    print(is_value_of_type(1, int))
    print(is_value_of_type(1, float))
    print(is_value_of_type([], list))
    print(is_value_of_type((), tuple))
    print(is_value_of_type({}, typing.NewType('Dict', dict)))
    print(is_value_of_type({}, dict[str, int, bool]))
    print(is_value_of_type([1, 2, 3], list[int, int, float]))
    print(is_value_of_type([1, 2, 3], list))
    print(is_value_of_type([1, 2, 3], list))
    print(is_value_of_type((1, 2, 3), tuple[int, ...]))
    """
    print(is_value_of_type({}, dict[str, list[set[int]]] | None))
