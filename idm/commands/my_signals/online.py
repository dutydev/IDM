from ...objects import dp, MySignalEvent, DB
from ... import utils
from threading import Thread, Timer
import time
from vkapi import VkApi
import typing

import logging

logger = logging.getLogger(__name__)

online_thread: Thread = None
stop_thread = False

def set_online(v):
    global stop_thread
    db = DB()
    stop_thread = v
    if v == False:
        api = VkApi(db.online_token)
        afa_thread = Thread(target=online_th, args=(api, lambda:stop_thread))
        afa_thread.setDaemon(True)
        afa_thread.setName('Online Thread')
        afa_thread.start()


def online_th(api: VkApi, stop: typing.Callable):
    is_stop = False
    while True:
        try:   
            if is_stop:break
            logger.info("Установлен онлайн")
            api('account.setOnline', voip=0)
            for _ in range(60):
                is_stop = stop()
                if is_stop:break
                time.sleep(5)
        except Exception as e:
            logger.info(f"Ошибка в online: {e}")



@dp.my_signal_event_handle('-онлайн')
def off_online(event: MySignalEvent):
    global online_thread
    global stop_thread

    logger.info("Выключен онлайн")

    if online_thread == None or not online_thread.is_alive():
        utils.new_message(event.api, event.chat.peer_id, message="❗ Вечный онлайн не запущен")
        return "ok"
    stop_thread = True
    # online_thread.join()
    utils.new_message(event.api, event.chat.peer_id, message="✅ Вечный онлайн остановлен.")
    return "ok"
    

@dp.my_signal_event_handle('+онлайн')
def on_online(event: MySignalEvent):
    global online_thread
    global stop_thread

    logger.info("Установлен онлайн")

    stop_thread = False
    token = event.db.online_token
    if token == None:
        utils.new_message(event.api, event.chat.peer_id, message=f"❗ Токен не установлен.\n Устанувить можно в админ-панеле https://{event.db.host}")
        return "ok"
    if online_thread != None and online_thread.is_alive():
        utils.new_message(event.api, event.chat.peer_id, message="✅ Вечный онлайн  и так запущен.")
        return "ok"
    api_ = VkApi(token)
    online_thread = Thread(target=online_th, args=(api_, lambda:stop_thread))
    online_thread.setDaemon(True)
    online_thread.setName('Online Thread')
    online_thread.start()
    utils.new_message(event.api, event.chat.peer_id, message="✅ Вечный онлайн запущен.")
    return "ok"

@dp.my_signal_event_handle('онлайн')
def check_online(event: MySignalEvent):
    global online_thread
    if online_thread != None and online_thread.is_alive():
        utils.new_message(event.api, event.chat.peer_id, message="✅ Вечный онлайн работает.")
        return "ok"
    else:
        utils.new_message(event.api, event.chat.peer_id, message="✅ Вечный онлайн не работает.")
        return "ok"