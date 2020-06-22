from .. import utils
from ..objects import dp, Event
from microvk import VkApi, VkApiResponseException

@dp.event_handle('subscribeSignals')
def subscribe_signals(event: Event) -> str:
    message = event.responses['chat_subscribe'].format(имя = event.chat.name,
    ид = event.chat.iris_id)
    event.db.chats[event.chat.iris_id]['installed'] = True
    event.db.save()
    utils.new_message(event.api, event.chat.peer_id, message=message)
    return "ok"