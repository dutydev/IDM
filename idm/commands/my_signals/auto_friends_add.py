from ...objects import dp, MySignalEvent, DB
from ... import utils
from threading import Thread, Timer
import time
from vkapi import VkApi, VkApiResponseException
import typing

import logging

logger = logging.getLogger(__name__)

afa_thread: Thread = None
stop_thread = False

def set_afa(v):
    global stop_thread
    global afa_thread
    
    db = DB()
    stop_thread = v
    if v == False:
        api = VkApi(db.access_token)
        afa_thread = Thread(target=afa_th, args=(api, lambda:stop_thread))
        afa_thread.setDaemon(True)
        afa_thread.setName('AFA Thread')
        afa_thread.start()

    

def afa_th(api: VkApi, stop: typing.Callable):
    is_stop = False
    while True:
        try:     
            if is_stop:break
            logger.info("Установлен онлайн")

            data = api('friends.getRequests', offset=0, count=1000, extended=0, need_mutual=0, out=0, need_viewed=1)['items']
            users = api('users.get', user_ids=",".join([str(i) for i in data]))

            for user in users:
                if user.get('deactivated', None) != None:
                    continue
                try:
                    api("friends.add", user_id=user['id'])
                except VkApiResponseException as e:
                    logger.error(f'Ошибка добавления пользвателя в друзья. {e.error_code} {e.error_msg} {e.request_params}')
                time.sleep(5)
                is_stop = stop()
                if is_stop:break
        except Exception as e:
            logger.info(f"Ошибка в AFA: {e}")
        time.sleep(300)


@dp.my_signal_event_handle('-адвд', '-друзья')
def off_afa(event: MySignalEvent):
    global afa_thread
    global stop_thread

    logger.info("Выключено автодобавление в друзья")

    if afa_thread == None or not afa_thread.is_alive():
        utils.new_message(event.api, event.chat.peer_id, message="❗ Автодобавление в друзья не запущено")
        return "ok"
    set_afa(False)
    utils.new_message(event.api, event.chat.peer_id, message="✅ Автодобавление в друзья остановлено.")
    return "ok"
    

@dp.my_signal_event_handle('+адвд', '+друзья')
def on_afa(event: MySignalEvent):
    global afa_thread
    global stop_thread

    logger.info("Установлен онлайн")

    stop_thread = False
    if afa_thread != None and afa_thread.is_alive():
        utils.new_message(event.api, event.chat.peer_id, message="✅ Автодобавление в друзья и так запущено.")
        return "ok"
    set_afa(True)
    utils.new_message(event.api, event.chat.peer_id, message="✅ Автодобавление в друзья запущено.")
    return "ok"

@dp.my_signal_event_handle('адвд', 'друзья')
def check_afa(event: MySignalEvent):
    global afa_thread
    if afa_thread != None and afa_thread.is_alive():
        utils.new_message(event.api, event.chat.peer_id, message="✅ Автодобавление в друзья работает.")
        return "ok"
    else:
        utils.new_message(event.api, event.chat.peer_id, message="✅ Автодобавление в друзья не работает.")
        return "ok"