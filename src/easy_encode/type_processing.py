import typing


def find_supertype(given_type):
    """go up the chain of given_type NewType definitions until we reach the base"""

    while type(given_type) == typing.NewType:
        given_type = given_type.__supertype__
    return given_type


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
