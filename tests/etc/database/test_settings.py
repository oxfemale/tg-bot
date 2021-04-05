from tg_bot.etc.database import models, settings


def test_get():
    response = settings.get()
    assert isinstance(response, models.TgBotSettings)
    assert 1 == response.id
