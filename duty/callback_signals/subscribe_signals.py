from duty.objects import dp, Event
from duty.utils import format_response


@dp.event_register('subscribeSignals')
def subscribe_signals(event: Event) -> str:
    message = format_response(
        event.responses['chat_subscribe'],
        имя=event.chat.name, ид=event.chat.iris_id
    )
    event.db.chats[event.chat.iris_id]['installed'] = True
    event.api.msg_op(1, event.chat.peer_id, message)
    return "ok"