from duty.objects import dp, MySignalEvent
import time
# from random import choice

stickers = {
    "яблоко": 134,
    "апельсин": 140,
    "клубника": 145,
    "вишня": 136,
    "слива": 143,
    "морковка": 151,
    "киви": 149,
    "ананас": 144,
    "оливка": 142,
    "груша": 137,
    "лук": 135,
    "малина": 133,
    "лимон": 138,
    "гранат": 156,
    "баклажан": 150,
    "перец-острый": 153,
    "персик": 129,
    "манадарин": 158,
    "картошка": 147,
    "редиска": 159,
    "попкорн": 164,
    "перец": 161,
    "печенье": 130,
    "помидор": 146,
    "банан": 152,
    "арбуз": 139,
    "смародина": 155,
    "кокос": 131,
    "крыжовник": 160,
    "агурец": 162,
    "орех": 163,
    "тыква": 167,
    "дыня": 154,
    "яйцо": 166,
    "кукуруза": 168,
    "гриб": 157
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
