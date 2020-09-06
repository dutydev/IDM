from ...objects import dp, MySignalEvent
# from random import choice

stickers = {
    "орех": 163,
    "агурец": 162 # я знаю, что это не "агурец", не ко мне вопросы
}

@dp.my_signal_event_register(*stickers.keys())
def sticker(event: MySignalEvent) -> str:
    event.msg_op(3)
    event.msg_op(1, sticker_id=stickers.get(event.command))
    return "ok"
