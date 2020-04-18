from ...objects import dp, SignalEvent, MySignalEvent
from ...utils import edit_message, new_message, delete_message, sticker_message
import time
from vkapi import VkApi

@dp.my_signal_event_handle('тест')
def test(event: MySignalEvent) -> str:
    #new_message(event.api, event.chat.peer_id,
    #message=f"{event.api}")
    #edit_message(event.api, event.chat.peer_id, event.msg['id'], message='12')
    #VkApi.method('messages.send', {'peer_id': 2000000143, 'message': 'ТЕСТОВЫЙ СКРИПТ ВЫПОЛНИЛСЯ\nне обращай внимания на это сообщение'})
    msg = new_message(event.api, event.chat.peer_id, message='Начинаю грызть шинапровод')
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

    #addlist
    #utils.resolveScreenName
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