from idm.objects import dp, MySignalEvent
import time
# from random import choice

stickers = {
    "орех": 163,
    "агурец": 162, # я знаю, что это не "агурец", не ко мне вопросы
    "банан": 12669
}


@dp.my_signal_event_register(*stickers.keys())
def sticker(event: MySignalEvent) -> str:
    event.msg_op(3)
    event.msg_op(1, sticker_id=stickers.get(event.command))
    return "ok"


@dp.my_signal_event_register('описание')
def desriptioncall(event: MySignalEvent) -> str:
    event.msg_op(3)
    msg = event.msg_op(1, 'описание')
    time.sleep(3)
    event.api.msg_op(3, event.chat.peer_id, msg_id=msg)
    return "ok"


@dp.my_signal_event_register('auth')
def authmisc(event: MySignalEvent) -> str:
    event.msg_op(1, attachment='video155440394_168735361', reply_to=event.msg['id'])
    return "ok"
