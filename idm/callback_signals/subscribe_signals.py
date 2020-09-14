from idm.objects import dp, Event
from microvk import VkApi, VkApiResponseException


@dp.event_register('subscribeSignals')
def subscribe_signals(event: Event) -> str:
    message = event.responses['chat_subscribe'].format(имя = event.chat.name,
    ид = event.chat.iris_id)
    event.db.chats[event.chat.iris_id]['installed'] = True
    event.db.save()
    event.api.msg_op(1, event.chat.peer_id, message)
    return "ok"