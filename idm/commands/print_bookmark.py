from .. import utils
from ..objects import dp, Event
from vkapi import VkApiResponseException

@dp.event_handle(dp.Methods.PRINT_BOOKMARK)
def print_bookmark(event: Event) -> str:
    utils.new_message(event.api, event.chat.peer_id, message=event.obj['description'],
        reply_to=utils.get_msg_id(event.api, event.chat.peer_id, event.obj['conversation_message_id']))
    return "ok"