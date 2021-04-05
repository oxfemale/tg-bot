import bit_help
import wrapcache

# Библы из папок
from tg_bot.etc import utils
from tg_bot.etc.conf import settings
from tg_bot.etc.database import settings as in_db_settings


class Bitcoin(bit_help.markets.Coinbase):
    def __init__(self, api_key=None, secret_key=None, bot_id=settings.BOT_ID):
        if api_key is None and secret_key is None:
            coinbase_data = in_db_settings.get()
            api_key = coinbase_data.coinbase_api_key
            secret_key = coinbase_data.coinbase_secret_key

        self.bot_id = bot_id

        super().__init__(api_key, secret_key)  # Это для bit-help

    def create_address(self, **kwargs):
        data = super().create_address(self.account_id)
        response = utils.Object()

        response.address_id = data["id"]
        response.address = data["address"]

        return response

    def balance(self):
        _balance = super().get_primary_account()["balance"]["amount"]
        _balance = float(_balance)
        return _balance

    def convert(self, currency, _sum, btc_price=None):
        btc_price = btc_price if btc_price is not None else self.price()

        if currency == "rub":
            _sum = round(_sum / btc_price, 8)

        elif currency == "btc":
            _sum = round(btc_price * _sum, 2)

        elif currency == "sts":
            ln = 8 - len(str(_sum))  # Сколько нулей нужно ещё до 8
            _sum = "0.{}{}".format("0" * ln, _sum)  # И создаётся сумма с нулями
            _sum = float(_sum)

        return _sum

    def get_last_payment(self, address_id):
        refill_sum = super().address_balance(address_id, confirmations=settings.NEED_BITCOIN_CONFIRMATIONS)
        return refill_sum

    @classmethod
    @wrapcache.wrapcache(timeout=300)
    def price(cls, currency=None):
        currency = currency if currency is not None else in_db_settings.get(bot_id=self.bot_id).fiat_currency
        return cls()._get_bitcoin_price(currency)

    def send_money(self, btc_address, _sum, now_currency="btc"):
        if "usd" == now_currency:
            _sum = self.convert("rub", _sum)

        super().send_money(btc_address, _sum)

    def _get_bitcoin_price(self, currency):
        price = super().price(currency=currency)
        return price
