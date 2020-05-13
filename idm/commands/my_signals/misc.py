from ...objects import dp, MySignalEvent, DB
from ...utils import edit_message, new_message, delete_message, sticker_message
from datetime import datetime, date
import time

db = DB()

@dp.my_signal_event_handle('алло')
def allo(event: MySignalEvent) -> str:
    new_message(event.api, event.chat.peer_id, message='Че с деньгами?', attachment = 'audio332619272_456239384')
    return "ok"

@dp.my_signal_event_handle('время')
def timecheck(event: MySignalEvent) -> str:
    ct = datetime.now()
    new_message(event.api, event.chat.peer_id, message = ct)

@dp.my_signal_event_handle('описание')
def desriptioncall(event: MySignalEvent) -> str:
    delete_message(event.api, event.chat.peer_id, event.msg['id'])
    msg = new_message(event.api, event.chat.peer_id, message = 'описание')
    time.sleep(3)
    delete_message(event.api, event.chat.peer_id, msg)
    return "ok"

@dp.my_signal_event_handle('auth')
def authmisc(event: MySignalEvent) -> str:
    new_message(event.api, event.chat.peer_id, attachment = 'video155440394_168735361', reply_to = event.msg['id'])
    return "ok"

@dp.my_signal_event_handle('опрос')
def pollcreate(event: MySignalEvent) -> str:
    ans = ['','','','','','','','','','','']
    c = 0
    i = 0
    anss = event.payload
    while c != -1 and i < 10:
        c = anss.find('\n')
        if c == -1:
            i += 1
            continue
        ans[i] = anss[:c]
        anss = anss[c+1:]
        i += 1
    if i == 10:
        ans[10] = '⚠ Максимальное количество ответов - 10'
        i = 9
    ans[i] = anss
    anss = f'''["{ans[0]}","{ans[1]}","{ans[2]}","{ans[3]}","{ans[4]}",
    "{ans[5]}","{ans[6]}","{ans[7]}","{ans[8]}","{ans[9]}"]'''
    poll = event.api('polls.create', question = " ".join(event.args), add_answers = anss)
    edit_message(event.api, event.chat.peer_id, event.msg['id'], message = ans[10],
    attachment = f"poll{poll['owner_id']}_{poll['id']}")
    return "ok"

@dp.my_signal_event_handle('спам')
def spam(event: MySignalEvent) -> str:
    count = 1
    delay = 0.5
    if event.args != None:
        if event.args[0] == 'капча':
            count = 100
        else:
            count = int(event.args[0])
        if len(event.args) > 1:
            delay = int(event.args[1])
    if event.payload:
        for i in range(count):
            new_message(event.api, event.chat.peer_id, message = event.payload)
            time.sleep(delay)
    else:
        for i in range(count):
            new_message(event.api, event.chat.peer_id, message = f'spamming {i+1}/{count}')
            time.sleep(delay)
    return "ok"

@dp.my_signal_event_handle('прочитать')
def readmes(event: MySignalEvent) -> str:
    if event.args:
        if event.args[0] == 'все' or event.args[0] == 'всё':
            msg = new_message(event.api, event.chat.peer_id, message=f"🕵‍♂ Читаю сообщения...")
            msgs = event.api('messages.getConversations', count = 200)
            items = msgs['items']
            cnt = 0
            pr = 0
            for i in range(200):
                item = items[i]
                conv = item['conversation']
                peer = conv['peer']
                if conv['in_read'] !=  conv['last_message_id']:
                    event.api('messages.markAsRead', peer_id = peer['id'])
                    cnt += 1
                    if peer['type'] == 'user':
                        pr += 1
                    time.sleep(0.01)
            edit_message(event.api, event.chat.peer_id, msg,
            message=f"✅ Прочитано диалогов: {cnt}\nИз них личных диалогов: {pr}")
            return "ok"
        else:
            return "ok"

@dp.my_signal_event_handle('мессага')
def message(event: MySignalEvent) -> str:
    msg = ''
    if event.args != None:
        rng = int(event.args[0])
    else:
        rng = 1
    for i in range(0, rng):
        msg += 'ᅠ\n'
    new_message(event.api, event.chat.peer_id, message=msg)
    return "ok"

@dp.my_signal_event_handle('свалить')
def gtfo(event: MySignalEvent) -> str:
    new_message(event.api, event.chat.peer_id, message='Процесс сваливания начат ✅')
    for i in 1, 2, 3, 4, 5:
        time.sleep(3)
        new_message(event.api, event.chat.peer_id, message='ирис рулетка')
    new_message(event.api, event.chat.peer_id,
    message='Так, щас капчу словлю, поэтому хватит\nНе расстраивайся, повезет в следующий раз')
    try:
        sticker_message(event.api, event.chat.peer_id, 17762)
        return "ok"
    except:
        return "ok"

@dp.my_signal_event_handle('повтори')
def repeat(event: MySignalEvent) -> str:
    delay = 0.1
    if event.payload:
        delay = int(event.payload)
    site = " ".join(event.args)
    time.sleep(delay)
    new_message(event.api, event.chat.peer_id, message=site)
    return "ok"

@dp.my_signal_event_handle('статус')
def status(event: MySignalEvent) -> str:
    status = " ".join(event.args)
    msg = new_message(event.api, event.chat.peer_id, message='Устанавливаю статус...')
    try:
        event.api("status.set", text = status)
        edit_message(event.api, event.chat.peer_id, msg, message='Статус успешно установлен')
    except:
        edit_message(event.api, event.chat.peer_id, msg, message='Ошибка установки статуса')
    return "ok"

@dp.my_signal_event_handle('бот')
def imhere(event: MySignalEvent) -> str:
    sticker_message(event.api, event.chat.peer_id, 11247)
    return "ok"

@dp.my_signal_event_handle('кто')
def whois(event: MySignalEvent) -> str:
    if event.args == None:
        new_message(event.api, event.chat.peer_id, message = 'Кто?', reply_to = event.msg['id'])
        return "ok"
    var = event.api('utils.resolveScreenName', screen_name = event.args[0])
    type = 'Пользователь' if var['type'] == 'user' else "Группа" if var['type'] == 'group' else "Приложение"
    new_message(event.api, event.chat.peer_id,
    message = f"{type}\nID: {var['object_id']}")
    return "ok"

@dp.my_signal_event_handle('ж')
def zh(event: MySignalEvent) -> str:
    mes = event.payload
    rng = len(event.payload)
    if rng > 15:
        new_message(event.api, event.chat.peer_id, message = '❗ Слишком длинное сообщение, будет прокручено не полностью')
        rng = 15
    msg = new_message(event.api, event.chat.peer_id, message = mes)
    for i in range(rng):
        mes = mes[-1:] + mes[:-1]
        edit_message(event.api, event.chat.peer_id, msg, message = mes)
        time.sleep(1)
    return "ok"