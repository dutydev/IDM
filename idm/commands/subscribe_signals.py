from .. import utils
from ..objects import dp, Event
from vkapi import VkApi, VkApiResponseException

@dp.event_handle(dp.Methods.SUBSCRIBE_SIGNALS)
def subscribe_signals(event: Event) -> str:
    #sticker_id = 19173
    message = f"""РАБОТАЕТ 👍
        Идентификатор чатика: {event.chat.iris_id}
        """.replace("    ", "")

    event.db.chats[event.chat.iris_id]['installed'] = True
    event.db.save()
    utils.new_message(event.api, event.chat.peer_id, message=message)
    return "ok"