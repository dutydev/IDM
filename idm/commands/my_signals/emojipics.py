from ...objects import dp, MySignalEvent
from ...utils import edit_message, new_message
import time

def anim_reply(reply_msg, vk):
    if reply_msg:
        user = vk('users.get', user_ids=reply_msg['from_id'])[0]
        msg = f"[id{user['id']}|{user['first_name']} {user['last_name']}]"
    else:
        msg = ''
    return msg

@dp.my_signal_event_handle('ф', 'f')
def fpic(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    picl = ['🌕🌗🌑🌑🌑🌑🌑🌓🌕','🌕🌗🌑🌑🌑🌑🌑🌕🌕','🌕🌗🌑🌓🌕🌕🌕🌕🌕','🌕🌗🌑🌓🌕🌕🌕🌕🌕',
    '🌕🌗🌑🌑🌑🌑🌓🌕🌕','🌕🌗🌑🌑🌑🌑🌕🌕🌕','🌕🌗🌑🌓🌕🌕🌕🌕🌕','🌕🌗🌑🌓🌕🌕🌕🌕🌕','🌕🌗🌑🌓🌕🌕🌕🌕🌕']
    pic0 = picl[0]
    pic1 = picl[1]
    pic2 = picl[2]
    pic3 = picl[3]
    pic4 = picl[4]
    pic5 = picl[5]
    pic6 = picl[6]
    pic7 = picl[7]
    pic8 = picl[8]

    for i in range(10):
        edit_message(event.api, event.chat.peer_id, event.msg['id'],
        message=f'''{msg}\n\n{pic0}\n{pic1}\n{pic2}\n{pic3}\n{pic4}
            {pic5}\n{pic6}\n{pic7}\n{pic8}'''.replace('    ', ''))
        pic0 = pic0[-1:] + pic0[:-1]
        pic1 = pic1[-1:] + pic1[:-1]
        pic2 = pic2[-1:] + pic2[:-1]
        pic3 = pic3[-1:] + pic3[:-1]
        pic4 = pic4[-1:] + pic4[:-1]
        pic5 = pic5[-1:] + pic5[:-1]
        pic6 = pic6[-1:] + pic6[:-1]
        pic7 = pic7[-1:] + pic7[:-1]
        pic8 = pic8[-1:] + pic8[:-1]
        time.sleep(0.8)
    return "ok"

@dp.my_signal_event_handle('луна')
def notthisdezh(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    edit_message(event.api, event.chat.peer_id, event.msg['id'], message='⚠ Не в этом дежурном')
    time.sleep(3)
    edit_message(event.api, event.chat.peer_id, event.msg['id'], message='Ладно, хорошо, так уж и быть...')
    time.sleep(2)
    pic = '🌑🌒🌓🌔🌕🌖🌗🌘'
    for i in range(9):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic}')
        pic = pic[-1:] + pic[:-1]
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('ъуъ')
def jujpic(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    picl = [
'🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕','🌕🌕🌕🌕🌕🌕🌕🌕🌕🌕','🌘🌑🌕🌕🌘🌑🌒🌕🌕🌕',
'🌑🌕🌕🌘🌑🌑🌑🌓🌕🌕','🌘🌔🌖🌑👁🌑👁🌓🌗🌒','🌖🌓🌗🌑🌑🌑🌑🌔🌕🌑',
'🌕🌗🌑🌑🌑🌑🌒🌕🌘🌒','🌕🌕🌘🌑🌑🌑🌑🌑🌒🌕','🌕🌕🌘🌑🌑🌑🌔🌕🌕🌕',
'🌕🌕🌘🌔🌘🌑🌕🌕🌕🌕','🌕🌖🌒🌕🌗🌒🌕🌕🌕🌕','🌕🌗🌓🌕🌗🌓🌕🌕🌕🌕']
    pic0 = picl[0]
    pic1 = picl[1]
    pic2 = picl[2]
    pic3 = picl[3]
    pic4 = picl[4]
    pic5 = picl[5]
    pic6 = picl[6]
    pic7 = picl[7]
    pic8 = picl[8]
    pic9 = picl[9]
    pic10 = picl[10]
    pic11 = picl[11]

    for i in range(11):
        edit_message(event.api, event.chat.peer_id, event.msg['id'],
message=f'''{msg}\n\n{pic0}\n{pic1}\n{pic2}\n{pic3}\n{pic4}\n{pic5}\n{pic6}
            {pic7}\n{pic8}\n{pic9}\n{pic10}\n{pic11}'''.replace('    ', ''))
        pic0 = pic0[-1:] + pic0[:-1]
        pic1 = pic1[-1:] + pic1[:-1]
        pic2 = pic2[-1:] + pic2[:-1]
        pic3 = pic3[-1:] + pic3[:-1]
        pic4 = pic4[-1:] + pic4[:-1]
        pic5 = pic5[-1:] + pic5[:-1]
        pic6 = pic6[-1:] + pic6[:-1]
        pic7 = pic7[-1:] + pic7[:-1]
        pic8 = pic8[-1:] + pic8[:-1]
        pic9 = pic9[-1:] + pic9[:-1]
        pic10 = pic10[-1:] + pic10[:-1]
        pic11 = pic11[-1:] + pic11[:-1]
        time.sleep(0.8)
    return "ok"

@dp.my_signal_event_handle('бан')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😒    😈",
"😒⚠    😈",
"😒 ⚠   😈",
"😒  ⚠  😈",
"😒   ⚠ 😈",
"😏 👿"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('цем')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
        '😚 ❤ ᅠᅠᅠᅠᅠ 😔 ',
        '😚 ᅠ ❤ ᅠᅠᅠᅠ 😔 ',
        '😚 ᅠᅠ ❤ ᅠᅠᅠ 😔 ',
        '😚 ᅠᅠᅠ ❤ ᅠᅠ 😔 ',
        '😚 ᅠᅠᅠᅠ ❤ ᅠ 😔 ',
        '😚 ᅠᅠᅠᅠᅠᅠ ❤ 😔 ',
        '😚 ᅠᅠᅠᅠᅠᅠ ☺ ',
        '😊 ☺ '
        ]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('поддержка', 'помощь', 'под')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😉     😔 ",
"😉👍    😔 ",
"😉 👍   😔 ",
"😉  👍  😔 ",
"😉   👍 😔 ",
"😉    👍😨 ",
"😉👍😊"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('мол')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😍     😔 ",
"😍 ❤   😔 ",
"😍  ❤  😔 ",
"😍   ❤ 😳 ",
"😍    ❤😍 ",
"😘🤗",
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('дорога', 'дрг')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"🛤\n🛤\n🛤\n🛤\n🛤",
"🚆\n🛤\n🛤\n🛤\n🛤",
"🛤\n🚆\n🛤\n🛤\n🛤",
"🛤\n🛤\n🚆\n🛤\n🛤",
"🛤\n🛤\n🛤\n🚆\n🛤",
"🛤\n🛤\n🛤\n🛤\n🚆",
"🛤\n🛤\n🛤\n🛤\n🛤"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('бб')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😔      😆",
"😢      😆",
"😕      😂",
"🙂👉   😮",
"🙂👉🔥😣",
"😂     😵"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('секс')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😶     😶",
"😍     😍",
"😍👉   👌😍",
"😍 👉 👌 😍",
"😍  👉👌 😍",
"😍 👉 👌 😍",
"🤤     🤤"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('брак')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"🙋   🏃",
"💁💕  🚶",
"🙎  🎁🙇",
"🙎🎁  🙇",
"🙆💍 🎁🙇",
" 💕💏💕",
"💕 💑 💕",
"👫   ⛪",
"👫  ⛪",
"👫 ⛪",
"👫💒"
]

    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('удар')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😔     🤣",
"😤     😂",
"😡🤜    🤣",
"😡 🤜   😂",
"😡  🤜  🤣",
"😡   🤜 🤣",
"😡    🤜😣",
"😌     😵"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('полиция')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"     🚓",
"    🚓",
"   🚓",
"  🚓",
" 🚓",
"🚓",
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('пнуть')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😑👟     🤔",
"😑 👟    🤔",
"😑  👟   🤔",
"😑   👟  🤔",
"😑    👟 🤔",
"😏     👟🤕"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('свидание')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"💃    🕺",
" 💃  🕺 ",
"  💃🕺  ",
"  👫 🌇",
"   👫🌇",
"   💑🌇",
"   💏🌇"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('вселенная')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"🌑✨✨🌏✨✨✨",
"✨🌑✨🌍✨✨✨",
"✨✨🌑🌎✨✨✨",
"✨✨✨🌏🌕✨✨",
"✨✨✨🌍✨🌕✨",
"✨✨✨🌎✨✨🌕"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('привет')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😄🖐",
"😄👋",
"😄🖐",
"😄👋",
"😄🖐",
"😄👋"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('пока')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😁🖐 ",
"😐👋 ",
"😕🖐 ",
"😔👋 ",
"😔✋ ",
"😔👋 ",
"😔✋"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('письмо')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😊💬         😔",
"😊  💬       😔",
"😊    💬     😔",
"😊      💬   😔",
"😊         💬😔",
"😊         😃"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('смерть')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"🙁     😎",
"😤     😎",
"😡🔪    😎",
"😡 🔪   😯",
"😡  🔪  😧",
"😡   🔪 😧",
"😡    🔪😩",
"😁     😵"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('на')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    if event.args[0] != 'попей':
        return "ok"
    pic = [
"🙂      🙂",
"😦      🙂",
"😯      🙂",
"😗💦     🙂",
"😗 💦    🙂",
"😗  💦   🤔",
"😗   💦  😳",
"😁    💦 😦",
"😂     💦😪",
"😈      😵"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('пожалуйста')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"🤓     🤔",
"🤓    🚶",
"🤓   🚶",
"🤓  😦",
"🤓 🚶",
"🤓🤔",
"🗣😏",
"🤝"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('накормить')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"🤔     😒",
"🤔🍔    😒",
"😊 🍔   😒",
"😊  🍔  😲",
"😊   🍔 😲",
"😁    🍔🤤",
"😌🍔😋"
]

    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('пошел')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    if event.args[0] != 'нахуй':
        return "ok"
    pic = [
"😔      🤣",
"😡    🤣",
"😡 🖕    🤣",
"😏     😢",
"🤣     😭"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('бух')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😋    🍾",
"😄   🍾",
"😁  🍾",
"🤤 🍾",
"🤢",
"🤮"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('поцеловать')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😺     🙄",
"😺    🙄",
"😺   🙄",
"😺  🙄",
"😺 🙄",
"😺🙄",
"😽😍"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('выстрел')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😏 😣",
"😂 🔫😡",
"😨 • 🔫😡",
"😵💥 🔫😡"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('зарплата', 'зп')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
"😔     🙋‍♂",
"😔     💁‍♂💵",
"😔    💵💁‍♂",
"😔   💵💁‍♂",
"😔  💵💁‍♂",
"😔 💵💁‍♂",
"😔💵💁‍♂",
"😔💵🙋‍♂",
"😦💵",
"😁💵"
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('бомба')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
'😠        😝',
'😡        😝',
'😡👉💣     😝',
'😡 👉💣   😝',
'😡  👉💣   😝',
'😡   👉💣  😝',
'😡    👉💣 😝',
'😡     👉💣😝',
'😌     👉💣💀'
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"

@dp.my_signal_event_handle('таймер')
def BFanim(event: MySignalEvent) -> str:
    msg = anim_reply(event.reply_message, event.api)
    pic = [
'🔟',
'9️⃣',
'8️⃣',
'7️⃣',
'6️⃣',
'5️⃣',
'4️⃣',
'3️⃣',
'2️⃣',
'1️⃣',
'✅ Время вышло ✅',
]
    for i in range(len(pic)):
        edit_message(event.api, event.chat.peer_id, event.msg['id'], message=f'{msg}\n\n{pic[i]}')
        time.sleep(1)
    return "ok"








