import peewee


class ValidationError(Exception):
    pass


class TextField(peewee.TextField):
    def __init__(self, validators=(), *args, **kwargs):
        self.validators = validators

        super().__init__(*args, **kwargs)

    def db_value(self, value):
        if self.run_validators(value) is False:
            raise ValidationError(value)

        return value

    def run_validators(self, value):
        for validator in self.validators:
            if validator(value):
                response = True
            else:
                response = False

            return response
