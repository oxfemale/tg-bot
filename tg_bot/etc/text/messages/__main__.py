from . import message_text


def broadcast_completed(broadcast_id, broadcast_result):
    success = broadcast_result["success"]
    bot_block = broadcast_result["bot_block"]
    unsuccessful = broadcast_result["unsuccessful"]

    mes = message_text.broadcast_completed
    mes = mes.format(broadcast_id, success, unsuccessful, bot_block, broadcast_result["delete_account"])
    return mes
