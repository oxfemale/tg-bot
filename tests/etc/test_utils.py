from tg_bot.etc import utils


def test_sorted_dict():
    already_sorted_dict = {"b": 1, "nf": 4, "dg": 5, "tye": 7, "gth": 15}
    un_sorted_dict = {"tye": 7, "dg": 5,  "b": 1, "gth": 15, "nf": 4}

    assert already_sorted_dict == utils.sorted_dict(un_sorted_dict)


def test_get_key():
    dict_for_test = {"b": 1, "nf": 4, "dg": 5, "tye": 7, "gth": 15}
    assert "nf" == utils.get_key(dict_for_test, 4)
