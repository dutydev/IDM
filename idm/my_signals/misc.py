# TODO: о господи что за дерьмо
from idm.objects import dp, MySignalEvent, DB, db_gen
from idm.api_utils import get_last_th_msgs
from datetime import datetime, date, timezone, timedelta
import time, re, requests, os, io, json
from microvk import VkApi

@dp.longpoll_event_register('хелп', 'help') #Автор: https://vk.com/id570532674, Доработал: https://vk.com/id194861150
@dp.my_signal_event_register('хелп', 'help')
def a(event: MySignalEvent) -> str:
    event.msg_op(2, f''' 📗Команды IrCA Duty: vk.com/@ircaduty-comands
⚙ Установка: https://vk.cc/c3coi7
💻 Исходный код: https://vk.cc/bZPeP4
🔧 Установка LP: https://vk.cc/c3cpNq
📈 Команды LP: https://vk.cc/c3cpUH
📓 Ваша админ панель: {db_gen.host}
Если будет вопросы, то обратитесь к этим прекрасным людям - https://vk.com/id365530525
https://vk.com/id194861150
https://vk.com/id449770994''')
    return "ok"

@dp.my_signal_event_register('кража')
def little_theft(event: MySignalEvent) -> str:
    if not event.args[0].startswith('ав'): return "ok"
    event.msg_op(3)
    uid = event.reply_message['from_id']
    if not uid:
        return "ok"
    image_url = event.api('users.get', fields = 'photo_max_orig',
        user_ids = uid)[0]['photo_max_orig']
    image = io.BytesIO(requests.get(url = image_url).content)
    image.name = 'ava.jpg'
    upload_url = event.api('photos.getOwnerPhotoUploadServer')['upload_url']
    data = requests.post(upload_url, files = {'photo': image}).json()
    del(image)
    post_id = event.api('photos.saveOwnerPhoto', photo = data['photo'],
        hash = data['hash'], server = data['server'])['post_id']
    event.msg_op(1, '😑😑😑', attachment=f'wall{event.db.duty_id}_{post_id}')
    return "ok"


@dp.my_signal_event_register('пуши', 'уведы')
def mention_search(event: MySignalEvent):
    mention = f'[id{event.db.duty_id}|'
    msg_ids = []

    for msg in get_last_th_msgs(event.chat.peer_id, event.api):
        if event.time - msg['date'] >= 86400: break
        if mention in msg['text']:
            msg_ids.append(str(msg['id']))
    
    if not msg_ids: msg = 'Ничего не нашел 😟'
    else: msg = 'Собсна, вот что нашел за последние 24 часа:'

    event.msg_op(1, msg, forward_messages = ','.join(msg_ids))
    return "ok"


@dp.my_signal_event_register('ксмс')
def tosms(event: MySignalEvent):
    cm_id = re.search(r'\d+', event.msg['text'])[0]
    msg = event.api('messages.getByConversationMessageId',
                    conversation_message_ids=cm_id,
                    peer_id=event.chat.peer_id)['items']
    if msg:
        if msg[0].get('action'):
            event.msg_op(2, 'Это сообщение - действие, не могу переслать')
        else:
            event.msg_op(1, 'Вот ента:', forward_messages = msg[0]['id'])
    else:
        event.msg_op(2, '❗ ВК вернул пустой ответ')
    return "ok"


@dp.my_signal_event_register('алло')
def allo(event: MySignalEvent) -> str:
    event.msg_op(1, 'Че с деньгами?', attachment = 'audio332619272_456239384')
    return "ok"

@dp.longpoll_event_register('рестарт')
@dp.my_signal_event_register('рестарт')
def restart(event: MySignalEvent) -> str:
    import uwsgi
    uwsgi.reload()
    event.msg_op(2, '...в процессе...')
    return "ok"


@dp.my_signal_event_register('тест')
def test(event: MySignalEvent) -> dict:
    return {"response":"error","error_code":"0","error_message":"Опа, кастомки подвезли"}

@dp.longpoll_event_register('время')
@dp.my_signal_event_register('время')
def timecheck(event: MySignalEvent) -> str:
    ct = datetime.now(timezone(timedelta(hours=+3))).strftime("%d of %B %Y (%j day in year)\n%H:%M:%S (%I:%M %p)")
    event.msg_op(2, ct)
    return "ok"


@dp.my_signal_event_register('взлом')
def ass_crackin(event: MySignalEvent) -> str:
    if event.args[0] != 'жопы': return "ok"
    fail = True
    event.msg_op(2, '☝🏻 Начинаю взлом жопы...')
    time.sleep(1)
    event.msg_op(1, 'передать 1 [id332619272|челику]\nна пивас', disable_mentions=1)
    time.sleep(4)
    for msg in event.api('messages.getHistory', count=10, peer_id=event.chat.peer_id)['items']:
        if '🍬 [id332619272|' in msg['text']:
            fail = False
            event.msg_op(1, '💚 Взлом жопы прошел успешно')
            break
    if fail:
        event.msg_op(1, '👀 Взлом жопы прошел неудачно, ослабьте анальную защиту')
    return "ok"


@dp.my_signal_event_register('опрос')
def pollcreate(event: MySignalEvent) -> str:
    answers = event.payload.split('\n')
    if not answers:
        event.msg_op(2, 'Необходимо указать варианты ответов (с новой строки)')
        return
    if len(answers) > 10:
        answers = answers[:10]
        warning = '⚠️ Максимальное количество ответов - 10'
    else:
        warning = ''
    poll = event.api('polls.create', question=" ".join(event.args),
                 add_answers=json.dumps(answers, ensure_ascii=False))
    event.msg_op(2, warning, attachment=f"poll{poll['owner_id']}_{poll['id']}")
    return "ok"


@dp.my_signal_event_register('спам')
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
            event.msg_op(1, event.payload)
            time.sleep(delay)
    else:
        for i in range(count):
            event.msg_op(1, f'spamming {i+1}/{count}')
            time.sleep(delay)
    return "ok"

@dp.longpoll_event_register('прочитать')
@dp.my_signal_event_register('прочитать')
def readmes(event: MySignalEvent) -> str:
    restricted = {'user'}
    if event.args:
        if event.args[0].lower() in {'все', 'всё'}:
            restricted = set()
        elif event.args[0].lower() == 'беседы':
            restricted = {'group', 'user'}
        elif event.args[0].lower() == 'группы':
            restricted = {'chat', 'user'}
    event.msg_op(2, "🕵‍♂ Читаю сообщения...")
    convers = event.api('messages.getConversations', count=200)['items']
    chats = private = groups = 0
    to_read = []
    code = 'API.messages.markAsRead({"peer_id": %s});'
    to_execute = ''
    for conv in convers:
        conv = conv['conversation']
        if conv['in_read'] != conv['last_message_id']:
            if conv['peer']['type'] in restricted:
                continue
            to_read.append(conv['peer']['id'])
            if conv['peer']['type'] == 'chat': chats += 1
            elif conv['peer']['type'] == 'user': private += 1
            elif conv['peer']['type'] == 'group': groups += 1

    while len(to_read) > 0:
        for _ in range(25 if len(to_read) > 25 else len(to_read)):
            to_execute += code % to_read.pop()
        event.api.exe(to_execute, event.db.me_token)
        time.sleep(0.1)  # TODO: это вообще нужно на PA?
        to_execute = ''

    message = '✅ Диалоги прочитаны:'
    if chats: message += f'\nБеседы: {chats}'
    if private: message += f'\nЛичные: {private}'
    if groups: message += f'\nГруппы: {groups}'
    if message == '✅ Диалоги прочитаны:':
        message = '🤔 Непрочитанных сообщений нет'

    event.msg_op(2, message)
    return "ok"


@dp.my_signal_event_register('мессага')
def message(event: MySignalEvent) -> str:
    msg = ''
    if event.args != None:
        rng = int(event.args[0])
    else:
        rng = 1
    for _ in range(0, rng):
        msg += 'ᅠ\n'
    event.msg_op(1, msg)
    return "ok"


@dp.my_signal_event_register('свалить')
def gtfo(event: MySignalEvent) -> str:
    event.msg_op(1, 'Процесс сваливания начат ✅')
    for _ in 1, 2, 3, 4, 5:
        time.sleep(3)
        event.msg_op(1, 'ирис рулетка')
    event.msg_op(1, 'Так, щас капчу словлю, поэтому хватит\nНе расстраивайся, повезет в следующий раз')
    try:
        event.msg_op(1, sticker_id=17762)
    except:
        pass
    finally:
        return "ok"


@dp.my_signal_event_register('повтори')
def repeat(event: MySignalEvent) -> str:
    delay = 0.1
    if event.payload:
        delay = int(event.payload)
    site = " ".join(event.args)  # лол, а почему оно так называется?
    time.sleep(delay)
    event.msg_op(1, site)
    return "ok"

@dp.longpoll_event_register('статус')
@dp.my_signal_event_register('статус')
def status(event: MySignalEvent) -> str:
    status = " ".join(event.args) + ' ' + event.payload
    msg = event.msg_op(1, 'Устанавливаю статус...')
    try:
        event.api("status.set", text = status)
        event.msg_op(2, 'Статус успешно установлен')
    except:
        event.msg_op(2, 'Ошибка установки статуса')
    return "ok"


@dp.my_signal_event_register('бот')
def imhere(event: MySignalEvent) -> str:
    event.msg_op(1, sticker_id=11247)
    return "ok"


@dp.my_signal_event_register('кто')
def whois(event: MySignalEvent) -> str:
    if event.args == None:
        event.msg_op(1, 'Кто?', reply_to = event.msg['id'])
        return "ok"
    var = event.api('utils.resolveScreenName', screen_name = event.args[0])
    type = 'Пользователь' if var['type'] == 'user' else "Группа" if var['type'] == 'group' else "Приложение"
    event.msg_op(1, f"{type}\nID: {var['object_id']}")
    return "ok"


@dp.my_signal_event_register('ж')
def zh(event: MySignalEvent) -> str:
    mes = event.payload
    rng = len(event.payload)
    if rng > 15:
        event.msg_op(1, '❗ Слишком длинное сообщение, будет прокручено не полностью')
        rng = 15
    msg = event.msg_op(1, mes)
    for _ in range(rng):
        mes = mes[-1:] + mes[:-1]
        event.api.msg_op(2, event.chat.peer_id, mes, event.msg['id'])
        time.sleep(1)
    return "ok"
