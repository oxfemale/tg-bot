def fiat_currency_validator(value):
    if value not in ["rub", "usd"]:
        response = False
    else:
        response = True

    return response