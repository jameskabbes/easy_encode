from easy_encode import types as ee_types
import types
import typing
import collections.abc


def find_supertype(given_type):
    """go up the chain of given_type NewType definitions until we reach the base"""

    while type(given_type) == typing.NewType:
        given_type = given_type.__supertype__
    return given_type


def is_value_of_type_mapping(value: collections.abc.Mapping, given_type: ee_types.ObjectAttributeType, is_value_of_type_func: ee_types.IsValueOfTypeFunction) -> bool:
    """recursively check if the first key-value pair of Mapping object is of given_type"""

    nested_types = typing.get_args(given_type)
    for key in value.keys():

        # check key
        if len(nested_types) < 1:
            break
        if not is_value_of_type_func(key, nested_types[0]):
            return False

        # check value
        if len(nested_types) < 2:
            break
        if not is_value_of_type_func(value[key], nested_types[1]):
            return False

    return True


def is_value_of_type_iterable(value: collections.abc.Iterable, given_type: ee_types.ObjectAttributeType, is_value_of_type_func: ee_types.IsValueOfTypeFunction) -> bool:

    nested_types = typing.get_args(given_type)
    counter = 0
    for item in iter(value):
        if counter >= len(nested_types):
            break
        if not is_value_of_type_func(item, nested_types[counter]):
            return False

        counter += 1

    return True


NESTED_TYPE_CHECKING: dict[type, ee_types.IsValueOfTypeCollection] = {
    collections.abc.Mapping: is_value_of_type_mapping,
    collections.abc.Iterable: is_value_of_type_iterable,
}


def is_value_of_type_include_union(value: ee_types.ObjectAttributeValue, given_type: ee_types.ObjectAttributeType) -> bool:
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
                return NESTED_TYPE_CHECKING[nested_type](value, given_supertype, is_value_of_type_include_union)

    # not a nested type
    given_supertype_args = typing.get_args(given_supertype)
    print('args')
    print(given_supertype_args)

    # union type
    if len(given_supertype_args) > 1:
        for given_supertype_arg in given_supertype_args:
            if is_value_of_type_include_union(value, given_supertype_arg):
                return True
        return False
    else:
        return value_type == given_supertype or given_type == ...


def is_value_of_type_exclude_union(value: ee_types.ObjectAttributeValue, given_type: ee_types.ObjectAttributeType) -> bool:
    """recursively check if value is of type: given_type"""

    # strip down the user defined NewTypes
    given_supertype = find_supertype(given_type)

    # see if this is a nested Mapping (dict) or Iterable (dict,list,set,tuple)
    given_supertype_origin = typing.get_origin(given_supertype)
    if given_supertype_origin != None:
        for nested_type in (collections.abc.Mapping, collections.abc.Iterable):
            if issubclass(given_supertype_origin, nested_type):
                return NESTED_TYPE_CHECKING[nested_type](value, given_supertype, is_value_of_type_exclude_union)

    # not a nested type
    given_supertype_args = typing.get_args(given_supertype)

    # not a union type
    if len(given_supertype_args) == 0:
        return type(value) == given_supertype or given_type == ...

    else:
        return False


def find_first_match(value: ee_types.ObjectAttributeValue, given_type: ee_types.ObjectAttributeType) -> tuple[bool, ee_types.ObjectAttributeType | None]:
    """for NewType and Union types, navigate down the path until we find the first type that matches the type of value"""

    given_supertype = find_supertype(given_type)
    given_supertype_origin = typing.get_origin(given_supertype)

    # a union type
    if given_supertype_origin == typing.Union or given_supertype_origin == types.UnionType:

        # loop through each type of the union and see if that type matches
        for given_type_arg in typing.get_args(given_supertype):
            response = find_first_match(value, given_type_arg)
            if response[0]:
                return response
        return (False, None)

    # not a union type
    else:
        if is_value_of_type_exclude_union(value, given_type):
            return (True, given_type)

        else:
            return (False, None)


def is_type_of_type_exclude_union(primary_type) -> bool:
    pass


def is_type_of_type_include_union(primary_type) -> bool:
    pass


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
    print(is_value_of_type({}, dict[str, list[set[int]]] | None))
    """

    b = typing.NewType('b', list[int])

    a = typing.NewType('a', str | b)
    # print(is_value_of_type_include_union([True, True, True], a))

    print()
    a = find_first_match([1, 2, 3], int | a | type(None) | list[int])
    print('Match is: ', a)
