import time


from .models import Broadcast


def profile(broadcast_id):
    return Broadcast().get_or_none(id=broadcast_id)


def added_broadcast(starter_chat_id, text, recipients):
    Broadcast().create(starter_chat_id=starter_chat_id, text=text, recipients=recipients)


def get_turned_off_broadcasts():
    _turned_off_broadcasts = []

    interval = time.time() - 60 * 10

    for broadcast in Broadcast().select().where(Broadcast.last_send <= interval):
        if 0 < len(broadcast.recipients):
            _turned_off_broadcasts.append(broadcast)

    return _turned_off_broadcasts


def update_profile(broadcast_id, table_name, value):
    broadcast_profile = profile(broadcast_id)

    setattr(broadcast_profile, table_name, value)
    broadcast_profile.save()
