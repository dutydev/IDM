from ...objects import dp, SignalEvent, MySignalEvent
from ...utils import edit_message, new_message, delete_message, sticker_message

@dp.my_signal_event_handle('дебагхелп', 'debughelp')
def debughelp(event: MySignalEvent) -> str:
    if event.args[0] == None:
        new_message(event.api, event.chat.peer_id,
        message=f"""Справочник для псевдопрограммистов:
        (добавь после команды цифру из списка)
        1. Список атрибутов event (SignalEvent, MySignalEvent)

        Пока все, хули ты хотел?""")
        return "ok"
    if event.args[0] == 'signalevent' or event.args[0] == 1:
        new_message(event.api, event.chat.peer_id,
        message=f"""event.message:\n{event.message}\n\nevent.msg:\n{event.msg}\n\nevent.chat:\n{event.chat}\n
        event.command:\n{event.command}\n\nevent.args:\n{event.args}\n\nevent.payload:\n{event.payload}\n
        event.reply_message:\n{event.reply_message}""")
        return "ok"