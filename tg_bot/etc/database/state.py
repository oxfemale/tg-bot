from .models import State


def action_get(bot_id, chat, user, column):
    state = State().get_or_none(bot_id=bot_id, chat=chat, user=user)
    if state is not None:
        state = getattr(state, column)

    return state


def action_set(bot_id, chat, user, column, data):
    user_state = State().get_or_none(bot_id=bot_id, chat=chat, user=user)
    if user_state:
        setattr(user_state, column, data)
        user_state.save()
    else:
        state = State()
        state.bot_id = bot_id
        state.chat = chat
        state.user = user
        setattr(state, column, data)
        state.save()

    return True
