from .models import TgBotInfo


def update_data_amount_messages():
    info = TgBotInfo.get(id=1)
    info.amount_messages += 1
    info.save()


def update_data_amount_callbacks():
    info = TgBotInfo.get(id=1)
    info.amount_callbacks += 1
    info.save()
