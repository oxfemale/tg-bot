import random_data


from .models import CallbackDataFilter

def write_data(data):
    code = random_data.etc.password(length=64)
    CallbackDataFilter.create(code=code, data=data)
    return code


def get_data(code):
    data = CallbackDataFilter.get_or_none(code=code)
    if data is not None:
        data = data.data

    return data
