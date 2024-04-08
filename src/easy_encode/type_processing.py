import typing


def find_supertype(given_type):
    """go up the chain of given_type NewType definitions until we reach the base"""

    while type(given_type) == typing.NewType:
        given_type = given_type.__supertype__
    return given_type


def is_union_type(given_type) -> bool:
    return len(typing.get_args(given_type)) > 1


def is_value_of_type(value, given_type, check_contents: typing.Literal['one', 'all'] = 'one') -> bool:
    """recursively check if value is of type: given_type"""

    print(value)
    print(given_type)

    value_type = type(value)
    print(value_type)

    # strip down the user defined NewTypes
    given_supertype = find_supertype(given_type)

    # see if this is a nested dict, list, or tuple
    given_supertype_origin = typing.get_origin(given_supertype)
    if given_supertype_origin in (dict, list, tuple):
        print('Nested type')
        if given_supertype_origin == dict:
            # check key
            # check value
            pass
            return False

        if given_supertype_origin == list or given_supertype_origin == tuple:
            return False

    # not a nested type
    else:
        print('Not a nested type')
        given_supertype_args = typing.get_args(given_supertype)
        if len(given_supertype_args) > 1:
            print('union type')
            return value_type in (find_supertype(arg) for arg in given_supertype_args)
        else:
            print('not union type')
            return value_type == given_supertype


def find_priority_type(given_type):
    """for types that are a Union of other types, return the first one"""

    given_type_args = typing.get_args(given_type)
    print(given_type_args)
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


def inspect_nested_type(given_type, given_value):
    pass


def test():

    print(is_value_of_type(1, int))
    print(is_value_of_type(1, float))
    print(is_value_of_type([], list))
    print(is_value_of_type((), tuple))
    print(is_value_of_type([], list))
