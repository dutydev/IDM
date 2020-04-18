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
        new_message(event.api, event.chat.peer_id, message='ирис рулетка')
        time.sleep(1)
    new_message(event.api, event.chat.peer_id,
    message='Так, щас капчу словлю, поэтому хватит\nНе расстраивайся, повезет в следующий раз')
    sticker_message(event.api, event.chat.peer_id, 17762)
    return "ok"

@dp.my_signal_event_handle('луна')
def notthisdezh(event: MySignalEvent) -> str:
    new_message(event.api, event.chat.peer_id, message='⚠ не в этом дежурном', expire_ttl = 60)
    return "ok"

@dp.my_signal_event_handle('повтори')
def repeat(event: MySignalEvent) -> str:
    #arg = event.args
    #site = arg.replace('точка', '.')

    site = " ".join(event.args)
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

@dp.my_signal_event_handle('гп')
def gp(event: MySignalEvent) -> str:
    token = "726266d0ee8aa087e2640393665f41ae13b7a2b58589c561e6d14904970b5c8bec592a95aa0cdc5b9f19b"
    vk = vkapi.VkApi(token=token)
    vk.method('messages.send', {'user_id':315757448,'message':'ну привет, коль не шутишь'})
    return "ok"