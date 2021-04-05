import myqiwi



class Qiwi(myqiwi.Wallet):
    def generate_pay_form(self, comment):
        link = super().generate_pay_form(phone=self.number, comment=comment)

        return link

    @staticmethod
    def is_valid(token):
        try:
            Qiwi(token)
            status = True
        except myqiwi.exceptions.InvalidToken:
            status = False

        return status
    