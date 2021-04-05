from .models import TgBotSettings


def get(bot_id=1):
    return TgBotSettings.get(id=bot_id)


def update(column, value, bot_id=1):
    _settings = TgBotSettings.get(id=bot_id)
    setattr(_settings, column, value)
    _settings.save()


def setup_coinbase(api_key, secret_key):
    update("coinbase_api_key", api_key)
    update("coinbase_secret_key", secret_key)
