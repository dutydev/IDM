from ...objects import dp, SignalEvent, MySignalEvent
from ...utils import edit_message, new_message, delete_message, sticker_message
import time
from vkapi import VkApi


import logging
logger = logging.getLogger(__name__)



@dp.my_signal_event_handle('тест')
def test(event: MySignalEvent) -> str:
    return "ok"

def testtask():
    vkapi.method('messages.send', {'user_id': 315757448, 'message': 'ТЕСТОВЫЙ СКРИПТ ВЫПОЛНИЛСЯ\nне обращай внимания на это сообщение'})

@dp.my_signal_event_handle('сохранить')
def save(event: MySignalEvent) -> str:
    state = event.api('storage.set', key = event.args[0], value = event.payload)
    msg = new_message(event.api, event.chat.peer_id, message=f'state: {state}')
    return "ok"

@dp.my_signal_event_handle('загрузить')
def load(event: MySignalEvent) -> str:
    state = event.api('storage.get', key = event.args[0])
    msg = new_message(event.api, event.chat.peer_id, message=f'return:\n{state}')
    return "ok"

@dp.my_signal_event_handle('получить')
def get(event: MySignalEvent) -> str:
    message = event.api('messages.getById', message_ids = event.payload)
    new_message(event.api, event.chat.peer_id, message=f'return:\n{message}')
    return "ok"

@dp.my_signal_event_handle('монтест')
def monitoringtest(event: MySignalEvent) -> str:
    lp = event.api('messages.getLongPollServer', need_pts = 1)
    #new_message(event.api, event.chat.peer_id, message=f"Получен ts: {lp['ts']}")
    i = 0
    old_msg = ''
    while i < 5:
        msg = ''
        time.sleep(1)
        lph = event.api('messages.getLongPollHistory', ts = lp['ts'])
        #if (i % 5) == 0:
        lp = event.api('messages.getLongPollServer', need_pts = 1)
            #new_message(event.api, event.chat.peer_id, message=f"Новый ts: {lp['ts']}")
        msgs = lph['messages']
        items = msgs['items']
        for l in range(len(items)):
            item = items[l]
            if item['text']:
                msg += '\n' + item['text']
        i += 1
        msg = msg.replace(old_msg, '')
        if msg == '' or msg == '':
            msg = 'null'
        old_msg += msg
        new_message(event.api, event.chat.peer_id,
        message=msg)
    return "ok"
    #addlist
    #wall.createComment
    #
    #

    #message: dict
    #msg: dict
    #chat: Chat

    #command: str
    #args: list
    #payload: str

    #reply_message: dict