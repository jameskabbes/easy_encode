from easy_encode import types as ee_types
import types
import typing
import collections.abc


def find_supertype(given_type):
    """go up the chain of given_type NewType definitions until we reach the base"""

    while type(given_type) == typing.NewType:
        given_type = given_type.__supertype__
    return given_type


def is_type_of_type(primary_type, secondary_type) -> bool:
    """list[int] is of type list"""

    return True


def is_value_of_type(value, given_type, top_level_union: bool = False, allow_any: bool = True, allow_subclass: bool = True) -> tuple[bool, typing.Any]:
    """recursively check if the type of value is of 'given_type', option to count all union types as False, and not count typing.Any
    ([1,2,3], list[int]) = True
    ({1:2.0, 3:4.0}, dict[int, int] = False)
    """

    given_type_origin = typing.get_origin(given_type)
    if given_type_origin != None:

        nested_types = typing.get_args(given_type)

        # see if this is a Mapping (dict) or Iterable (dict,list,set,tuple)
        is_mapping = False
        try:
            is_mapping = issubclass(
                given_type_origin, collections.abc.MutableMapping)
        except:
            pass

        if is_mapping:
            mapping: collections.abc.MutableMapping = value
            for key in mapping.keys():

                # check key
                if len(nested_types) < 1:
                    break
                if not is_value_of_type(key, nested_types[0], top_level_union=top_level_union, allow_any=allow_any, allow_subclass=allow_subclass)[0]:
                    return (False, None)

                # check value
                if len(nested_types) < 2:
                    break
                if not is_value_of_type(mapping[key], nested_types[1], top_level_union=top_level_union, allow_any=allow_any, allow_subclass=allow_subclass)[0]:
                    return (False, None)

            return (True, given_type)

        is_iterable = False
        try:
            is_iterable = issubclass(
                given_type_origin, collections.abc.Iterable)
        except:
            pass

        if is_iterable:
            counter = 0
            for item in iter(value):
                if counter >= len(nested_types):
                    break
                if not is_value_of_type(item, nested_types[counter], top_level_union=top_level_union, allow_any=allow_any, allow_subclass=allow_subclass)[0]:
                    return (False, None)
                counter += 1

            return (True, given_type)

    # not a nested type
    given_type_args = typing.get_args(given_type)

    # a Union type
    if len(given_type_args) > 1:
        for given_type_arg in given_type_args:
            response = is_value_of_type(
                value, given_type_arg, top_level_union=top_level_union, allow_any=allow_any, allow_subclass=allow_subclass)

            # if anything from the union matches, return True
            if response[0]:
                if top_level_union:
                    return (True, given_type)
                else:
                    return response
        return (False, None)

    # some other wrapping type like typing.Required, typing.NotRequired, etc have get_args() of length 1
    elif len(given_type_args) == 1:

        return is_value_of_type(value, given_type_args[0], top_level_union=top_level_union, allow_any=allow_any, allow_subclass=allow_subclass)

        # Maybe recursively return this function call's given_type instead? Something like
        # if is_value_of_type(value, given_type_args[0], top_level_unions=top_level_unions)[0]:
        #    return (True, given_type)

    # this is a regular ole type, with no args
    elif len(given_type_args) == 0:

        raw_type = type(value)
        if raw_type == given_type or given_type == ... or (given_type == typing.Any and allow_any):
            return (True, given_type)

        # try it all again with the given types __supertype__
        if type(given_type) == typing.NewType:
            if is_value_of_type(value, given_type.__supertype__, top_level_union=top_level_union, allow_any=allow_any, allow_subclass=allow_subclass)[0]:
                return (True, given_type)
            return (False, None)

        if (issubclass(raw_type, given_type) and allow_subclass):
            return (True, given_type)

        return (False, None)


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

    def perform_test(expected_validity, value, type, **kwargs: ee_types.IsValueOfTypeFunctionKwargs):
        respone = is_value_of_type(value, type, **kwargs)
        print('value: {} type: {} valid: {} valid_type: {}'.format(
            value, type, respone[0], respone[1]))
        if expected_validity != respone[0]:
            print('====================')
            print('WARNING')
            print('====================')

    perform_test(True, True, bool)

    perform_test(True, True, bool)
    perform_test(True, 1, int)
    perform_test(True, 1.0, float)
    perform_test(False, None, bool)
    perform_test(False, None, int)
    perform_test(False, 1, float)
    perform_test(True, True, ...)
    perform_test(True, None, typing.Any, allow_any=True)
    perform_test(False, None, typing.Any, allow_any=False)
    perform_test(True, 1, float | int, top_level_union=True)
    perform_test(True, 1, float | int, top_level_union=False)
    perform_test(True, 1, typing.NewType('A', typing.NewType('B', int)))
    perform_test(False, 1.0, typing.NewType('A', typing.NewType('B', int)))
    perform_test(True, [1, 2, 3], list[int])
    perform_test(False, [1.0, 2, 3], list[int])
    perform_test(True, [1, 2.0, 3], list[int])
    perform_test(False, [1, 2.0, 3], list[int, int])
    perform_test(True, [1, 2, 3], collections.abc.Iterable[int])
    perform_test(True, [1, 2, 3], collections.abc.Iterable)
    perform_test(False, [1, 2, 3], collections.abc.Iterable[bool])
    perform_test(True, (1, 2, 3), tuple[int, ...])
    perform_test(True, (1, 2.0, 3), tuple[int, float])

    # not sure type safety should work this way
    perform_test(True, (1,), tuple[int, float])

    perform_test(True, {}, dict[str, list[set[int]]] | None)
