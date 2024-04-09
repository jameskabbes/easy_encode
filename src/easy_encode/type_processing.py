import typing


def find_supertype(given_type):
    """go up the chain of given_type NewType definitions until we reach the base"""

    while type(given_type) == typing.NewType:
        given_type = given_type.__supertype__
    return given_type


def is_value_of_type_dict(value: dict, given_type) -> bool:
    nested_types = typing.get_args(given_type)

    # empty dict passes
    if len(value) == 0:
        return True

    for i in range(max(len(nested_types), 2)):
        nested_type = nested_types[i]

        # check key
        first_key = list(value.keys())[0]
        if i == 0:
            if not is_value_of_type(first_key, nested_type):
                return False

        # check value
        if i == 1:
            if not is_value_of_type(value[first_key], nested_type):
                return False

    return True


def is_value_of_type_iterable(value: typing.Iterable, given_type) -> bool:
    nested_types = typing.get_args(given_type)

    for i in range(min(len(nested_types), len(value))):
        nested_type = nested_types[i]
        if not is_value_of_type(value[i], nested_type):
            return False

    return True


NESTED_TYPE_CHECKING: dict[type, typing.Callable] = {
    list: is_value_of_type_dict,
    tuple: is_value_of_type_iterable,
    list: is_value_of_type_iterable,
}


def is_value_of_type(value, given_type) -> bool:
    """recursively check if value is of type: given_type"""

    value_type = type(value)

    # strip down the user defined NewTypes
    given_supertype = find_supertype(given_type)

    # see if this is a nested dict, list, or tuple
    given_supertype_origin = typing.get_origin(given_supertype)
    if given_supertype_origin in NESTED_TYPE_CHECKING:
        return NESTED_TYPE_CHECKING[given_supertype_origin](value, given_type)

    # not a nested type
    else:
        given_supertype_args = typing.get_args(given_supertype)

        # union type
        if len(given_supertype_args) > 1:
            return value_type in (find_supertype(arg) for arg in given_supertype_args)
        else:
            return value_type == given_supertype


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

    print(is_value_of_type(True, bool))
    print(is_value_of_type(1, int))
    print(is_value_of_type(1, float))
    print(is_value_of_type([], list))
    print(is_value_of_type((), tuple))
    print(is_value_of_type({}, typing.NewType('Dict', dict)))
    print(is_value_of_type([1, 2, 3], list[int, int, float]))
    print(is_value_of_type([1, 2, 3], list))
    print(is_value_of_type([1, 2, 3], list))
