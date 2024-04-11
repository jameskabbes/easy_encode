from easy_encode import types as ee_types
import types
import typing
import collections.abc


def find_supertype(given_type):
    """go up the chain of given_type NewType definitions until we reach the base"""

    while type(given_type) == typing.NewType:
        given_type = given_type.__supertype__
    return given_type


default_is_value_of_type_kwargs: ee_types.IsValueOfTypeKwargs = {
    'allow_union': True,
    'allow_subclass': True,
    'allow_any': True
}


def is_value_of_type(value, given_type, **kwargs: ee_types.IsValueOfTypeKwargs) -> tuple[bool, typing.Any]:
    """recursively check if the type of value is of 'given_type', option to count all union types as False, and not count typing.Any
    ([1,2,3], list[int]) = True
    ({1:2.0, 3:4.0}, dict[int, int] = False)
    """

    allow_union = default_is_value_of_type_kwargs[
        'allow_union'] if 'allow_union' not in kwargs else kwargs['allow_union']
    allow_subclass = default_is_value_of_type_kwargs[
        'allow_subclass'] if 'allow_subclass' not in kwargs else kwargs['allow_subclass']
    allow_any = default_is_value_of_type_kwargs[
        'allow_any'] if 'allow_any' not in kwargs else kwargs['allow_any']

    given_type_origin = typing.get_origin(given_type)
    if given_type_origin != None:

        nested_types = typing.get_args(given_type)

        # see if this is a Mapping (dict) or Iterable (dict,list,set,tuple)
        if issubclass(given_type_origin, collections.abc.Mapping):
            mapping: collections.abc.Mapping = value
            for key in mapping.keys():

                # check key
                if len(nested_types) < 1:
                    break
                if not is_value_of_type(key, nested_types[0], **kwargs)[0]:
                    return (False, None)

                # check value
                if len(nested_types) < 2:
                    break
                if not is_value_of_type(mapping[key], nested_types[1], **kwargs)[0]:
                    return (False, None)

            return (True, given_type)

        elif issubclass(given_type_origin, collections.abc.Iterable):

            counter = 0
            for item in iter(value):
                if counter >= len(nested_types):
                    break
                if not is_value_of_type(item, nested_types[counter], **kwargs)[0]:
                    return (False, None)
                counter += 1

            return (True, given_type)

    # not a nested type
    given_type_args = typing.get_args(given_type)

    # a Union type
    if len(given_type_args) > 1:
        if allow_union:
            # if anything from the union matches, return True
            for given_type_arg in given_type_args:
                if is_value_of_type(value, given_type_arg, **kwargs):
                    return (True, given_type)
            return (False, None)

        else:
            return (False, None)

    # some other wrapping type like typing.Required, typing.NotRequired, etc have
    elif len(given_type_args) == 1:

        return is_value_of_type(value, given_type_args[0], **kwargs)

        # Maybe recursively return this function call's given_type instead? Something like
        # if is_value_of_type(value, given_type_args[0], allow_unions=allow_unions)[0]:
        #    return (True, given_type)

    # this is a regular ole type, with no args
    elif len(given_type_args) == 0:

        raw_type = type(value)
        if raw_type == given_type or given_type == ... or (given_type == typing.Any and allow_any):
            return (True, given_type)

        # try it all again with the given types __supertype__
        if hasattr(given_type, '__supertype__') and type(given_type) == typing.NewType:
            if is_value_of_type(value, given_type.__supertype__, **kwargs)[0]:
                return (True, given_type)
            return (False, None)

        if (issubclass(raw_type, given_type) and allow_subclass):
            return (True, given_type)

        return (False, None)


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
        if is_value_of_type(value, given_type, allow_unions=False):
            return (True, given_type)

        else:
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

    def perform_test(expected_validity, value, type, **kwargs: ee_types.IsValueOfTypeKwargs):
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
    perform_test(True, 1, float | int, allow_union=True)
    perform_test(False, 1, float | int, allow_union=False)
    perform_test(True, 1, float | int, allow_union=True)
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
