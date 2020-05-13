from ...objects import dp, SignalEvent, MySignalEvent, DB
from ...utils import edit_message, new_message, delete_message, sticker_message
from ...lp import IIS
import time
from vkapi import VkApi
from idm import __version__

import logging
logger = logging.getLogger(__name__)

def testtask():
    VkApi.method('messages.send', {'user_id': 315757448, 'message': 'ТЕСТОВЫЙ СКРИПТ ВЫПОЛНИЛСЯ\nне обращай внимания на это сообщение'})

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
    message = event.api('messages.getById',message_ids = event.payload)
    new_message(event.api, event.chat.peer_id, message=f'return:\n{message}')
    return "ok"

@dp.my_signal_event_handle('монтест')
def monitoringtest(event: MySignalEvent) -> str:
    delete_message(event.api, event.chat.peer_id, event.msg['id'])
    i = 0
    old_msg = ''
    msg = ''
    item = {"text": ""}
    last_msg = new_message(event.api, event.chat.peer_id, message='Наблюдаю 👀')
    while item['text'] != 'стоп':
        history = event.api('messages.getHistory', peer_id = event.chat.peer_id, count = 2)
        items = history['items']
        item = items[0]
        if item['text'] != old_msg and last_msg != item['id']:
            msg += '\n' + item['text']
            old_msg = item['text']
        if item['text'].find('скинь') != -1 and last_msg != item['id']:
            last_msg = new_message(event.api, event.chat.peer_id, message=msg)
            msg = ''
        i += 1
    new_message(event.api, event.chat.peer_id, message=msg)
    new_message(event.api, event.chat.peer_id, message=f'Итераций цикла: {i}')
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