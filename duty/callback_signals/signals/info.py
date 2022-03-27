from duty.objects import dp, SignalEvent, __version__
from duty.utils import ment_user, format_response
import time

@dp.signal_event_register('инфо', 'инфа', 'info')
def sinfo(event: SignalEvent) -> str:
    if event.msg['from_id'] not in event.db.trusted_users:
        message_id = event.send(event.responses['not_in_trusted'])
        time.sleep(3)
        event.api.msg_op(3, msg_id=message_id)
        return "ok"

    owner = event.api('users.get', user_ids=event.db.owner_id)[0]

    event.send(format_response(
        event.responses['info_duty'], 
        версия=__version__,
        владелец=ment_user(owner),
        чаты=len(event.db.chats.keys()),
        ид=event.chat.iris_id,
        имя=event.chat.name
    ))
    return "ok"
