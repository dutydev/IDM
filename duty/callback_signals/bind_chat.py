from duty.objects import dp, Event, Chat
from duty.utils import cmid_key, format_response


@dp.event_register('bindChat')
def bind_chat(event: Event) -> str:
    search_res = event.api("messages.search",
                           q=event.msg['text'], count=10, extended=1)
    for msg in search_res['items']:
        if msg[cmid_key] == event.msg[cmid_key]:
            if msg['from_id'] == event.msg['from_id']:
                message = msg
                break
    for conv in search_res['conversations']:
        if conv['peer']['id'] == message['peer_id']:  # type: ignore
            chat_name = conv['chat_settings']['title']
            break
    chat_raw = {
        "peer_id": message['peer_id'],  # type: ignore
        "name": chat_name,  # type: ignore
        "installed": False
    }
    event.db.chats.update({event.obj['chat']: chat_raw})
    event.chat = Chat(chat_raw, event.obj['chat'])
    event.send(format_response(event.responses['chat_bind'], имя=event.chat.name))
    return "ok"
