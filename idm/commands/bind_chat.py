from ..objects import dp, Event, MySignalEvent, DB, Chat
from ..lpcommands.utils import msg_op, get_msg
from microvk import VkApi

@dp.event_handle('bindChat')
def bind_chat(event: Event) -> str:
    for chat in event.api("messages.getConversations", count=100)['items']:
        diff = chat['last_message']['conversation_message_id'] - event.msg['conversation_message_id']
        if diff > 100 or diff < -100:
            continue
        conv = chat['conversation']
        if conv['peer']['type'] == "chat":
            message = event.api('messages.getByConversationMessageId', peer_id=conv['peer']['id'],
                conversation_message_ids=event.msg['conversation_message_id'])['items']
            if not message:
                continue
            if message[0]['from_id'] == event.msg['from_id'] and message[0]['date'] == event.msg['date']:
                chat_dict = { "peer_id": conv['peer']['id'],
                              "name": conv['chat_settings']['title'],
                              "installed": False }
                event.db.chats.update({event.obj['chat']: chat_dict})
                event.db.save()
                event.chat = Chat(chat_dict, event.obj['chat'])
                break
    msg_op(1, event.chat.peer_id, event.responses['chat_bind'].format(
    имя = event.chat.name))
    return "ok"