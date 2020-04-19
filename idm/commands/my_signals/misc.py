from ...objects import dp, MySignalEvent
from ...utils import edit_message, new_message, delete_message, sticker_message
from datetime import datetime, date
import time

@dp.my_signal_event_handle('алло')
def allo(event: MySignalEvent) -> str:
    new_message(event.api, event.chat.peer_id, message='Че с деньгами?', attachment = 'audio332619272_456239384')
    return "ok"

@dp.my_signal_event_handle('auth')
def authmisc(event: MySignalEvent) -> str:
    new_message(event.api, event.chat.peer_id, attachment = 'video155440394_168735361', reply_to = event.msg['id'])
    return "ok"

@dp.my_signal_event_handle('спам')
def spam(event: MySignalEvent) -> str:
    if event.args == None:
        count = 1
    elif event.args[0] == 'капча':
        count = 100
    else:
        count = int(event.args[0])
    for i in range(count):
        new_message(event.api, event.chat.peer_id, message = f'spamming {i+1}/{count}')
        time.sleep(0.5)
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
    time.sleep(0.5)
    new_message(event.api, event.chat.peer_id,
    message='Так, щас капчу словлю, поэтому хватит\nНе расстраивайся, повезет в следующий раз')
    sticker_message(event.api, event.chat.peer_id, 17762)
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

@dp.my_signal_event_handle('ирисразбан')#не доделано
def irisunban(event: MySignalEvent) -> str:
    c_time = datetime(2020, 4, 19)
    new_message(event.api, event.chat.peer_id, message=c_time)
    delta = round(c_time - event.msg['date'], 3)
    new_message(event.api, event.chat.peer_id, message=f'До разбана ириса осталось {delta}')

    today = date.today()
    today == date.fromtimestamp(time.time())
    my_birthday = date(today.year, 6, 24)
    my_birthday
    datetime.date(2008, 6, 24)
    time_to_birthday = abs(my_birthday - today)
    time_to_birthday.days

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

@dp.my_signal_event_handle('гп') #не доделано (да блядь, половина бота не доделана)
def gp(event: MySignalEvent) -> str:
    token = "726266d0ee8aa087e2640393665f41ae13b7a2b58589c561e6d14904970b5c8bec592a95aa0cdc5b9f19b"
    vk = vkapi.VkApi(token=token)
    vk.method('messages.send', {'user_id':315757448,'message':'ну привет, коль не шутишь'})
    return "ok"
