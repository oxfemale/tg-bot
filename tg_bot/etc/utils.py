import datetime


def sorted_dict(_list):
    new_list = {}

    _list = list(_list.items())
    _list.sort(key=lambda element: element[1])
    _list.reverse()

    for i in _list:
        new_list[i[0]] = i[1]

    return new_list


def get_key(dictionary, searched_value):
    for key, value in dictionary.items():
        if value == searched_value:
            return key


def get_variables_from_module(module):
    variables = []
    for object_name in dir(module):
        _object = getattr(module, object_name)
        if not object_name.startswith("__") and "module" != type(_object).__name__:
            variables.append([object_name, _object])

    return variables


class Object:
    pass