# да что ты вообще знаешь про костыли...
from ...objects import dp, MySignalEvent
from ...lpcommands import bomb, msg_del, dlp, ND
from ...lpcommands.anims import animation_names


def nd_adapt(event):
    return [0, event.msg['id'], 0, event.chat.peer_id, 0, event.msg['text'],
    0, {"reply": event.msg.get('reply_message')}]


@dp.my_signal_event_register('шабы', 'шаб', '+шаб', '-шаб', 'анимки', 'анимка',
'+анимка', '-анимка', '-конв', 'конв', '+др', '+друг', '-др', '-друг', '+чс',
'-чс', 'пуши', 'уведы', 'шрифт', 'шрифты', *animation_names)
def weird_bunch_of_commands(event: MySignalEvent) -> str:
    return dlp.launch(nd_adapt(event), event.db, event.api, event.time, event.msg)


@dp.my_signal_event_register('б')
def bombcb(event: MySignalEvent) -> str:
    return bomb(nd_adapt(event), event.db, event.api, event.msg)


@dp.my_signal_event_register('-смс')
def delete_self_message(event: MySignalEvent) -> str:
    return msg_del(nd_adapt(event), msg = event.responses['del_self'], vk = event.api)