import requests
from yandex_money import api


api.config["MONEY_URL"] = "https://yoomoney.ru"
api.config["SP_MONEY_URL"] = api.config["MONEY_URL"]


class QuickPayForm:
    shop = "shop"
    donate = "donate"


class YooMoney(api.Wallet):
    def __init__(self, access_token):
        super().__init__(access_token)

    def balance(self):
        return self.account_info()["balance"]

    @staticmethod
    def gen_payment_link(receiver, label, sum_, quickpay_form=QuickPayForm.donate, targets="Оплата услуг"):
        """
        https://yoomoney.ru/docs/payment-buttons/using-api/forms
        """

        url = "{}/quickpay/confirm.xml".format(api.config["MONEY_URL"])
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            "receiver": receiver,
            "quickpay-form": quickpay_form,
            "targets": targets,
            "label": label,
            "sum": sum_
            # 'paymentType': 'AC'
        }


        url = requests.post(url, data=data, headers=header).url
        return url

    @staticmethod
    def build_obtain_token_url(app_id, redirect_url="https://example.com/", *args):
        scope = ["account-info", "operation-history", "payment-p2p", "operation-details"]
        url = api.Wallet.build_obtain_token_url(app_id, redirect_url, scope=scope)
        return url

    @staticmethod
    def get_access_token(code, client_id, redirect_url="https://example.com/", *args):
        response = api.Wallet.get_access_token(code, client_id, redirect_url)
        return response["access_token"]

    def search_payment(self, need_comment, need_sum=0):
        refill_sum = 0
        operations = super().operation_history({})["operations"]
        for operation in operations:
            _sum = operation["amount"]
            is_direction_in = "in" == operation["direction"]

            if is_direction_in and "label" in operation and need_comment == operation["label"] and need_sum <= _sum:
                refill_sum += _sum

        return refill_sum

    def send_money(self, to, amount=None, amount_due=None, comment=None, message=None, label=None, codepro=None,
                   expire_period=None, pattern_id="p2p"):
        options = {
            "pattern_id": pattern_id,
            "to": str(to),
        }

        data = {
            "amount": amount,
            "amount_due": amount_due,
            "comment": comment,
            "message": message,
            "label": label,
            "codepro": codepro,
            "expire_period": expire_period,
        }

        for param_name, value in data.items():
            options = self.if_is_not_none_add(options, param_name, value)

        status = super().request_payment(options)
        return super().process_payment({"request_id": status["request_id"]})

    @staticmethod
    def if_is_not_none_add(dict_, key, value):
        if value is not None:
            dict_[key] = value

        return dict_
