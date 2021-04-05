from tg_bot.etc.pay import Bitcoin
from .models import TgBotBitcoinAddresses


def get_user_address(chat_id, response="address"):
    record = BitcoinAddresses.get_or_none(holder_chat_id=chat_id, using=False)

    if record is None:
        record = data = Bitcoin().create_address()
        BitcoinAddresses.create(holder_chat_id=chat_id, address=data.address, address_id=data.address_id)

    return getattr(record, response)


def update(address_id, column, value):
    address = BitcoinAddresses.get(address_id=address_id)
    setattr(address, column, value)
    address.save()


def check_user_payment(chat_id, minimum_sum=0.0001):
    address_id = get_user_address(chat_id, response="address_id")

    response = Bitcoin().get_last_payment(address_id)
    if minimum_sum < response:
        update(address_id, "using", True)
    else:
        response = 0

    return response

