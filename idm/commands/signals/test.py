from ...objects import dp, SignalEvent, MySignalEvent
from ...utils import edit_message, new_message, delete_message, sticker_message
import time

@dp.signal_event_handle('тест')
def test(event: SignalEvent) -> str:
    new_message(event.api, event.chat.peer_id, message='Тест отправки стикеров')
    sticker_message(event.api, event.chat.peer_id, 19173)
    return "ok"

@dp.my_signal_event_handle('тест')
def testMy(event: MySignalEvent) -> str:
    new_message(event.api, event.chat.peer_id, message='Тест отправки стикеров')
    sticker_message(event.api, event.chat.peer_id, 19173)
    return "ok"