from ...objects import dp, SignalEvent, MySignalEvent
from ...utils import edit_message, new_message, delete_message, sticker_message
from ...lp import IIS

@dp.my_signal_event_handle('дебагхелп', 'debughelp')
def debughelp(event: MySignalEvent) -> str:
    if event.args == None:
        new_message(event.api, event.chat.peer_id,
        message=f"""Справочник для псевдопрограммистов:
        (добавь после команды цифру из списка)
        1. Список атрибутов event (SignalEvent, MySignalEvent)

        Пока все, хули ты хотел?""")
        return "ok"
    elif event.args[0] == '1':
        new_message(event.api, event.chat.peer_id,
        message=f"""event.message:\n{event.message}\n\nevent.msg:\n{event.msg}\n\nevent.chat:\n{event.chat}\n
        event.command:\n{event.command}\n\nevent.args:\n{event.args}\n\nevent.payload:\n{event.payload}\n
        event.reply_message:\n{event.reply_message}\n\nevent.attachments:\n{event.attachments}\n
        event.secret:\nсекретный код дежурного, здесь, по ясным причинам, не скажу""")
        new_message(event.api, event.chat.peer_id,
        message=f"""event.event:\n{event.event}\n\nevent.api:\n{event.api}\n\nevent.db:\n{event.db}
        \nevent.method:\n{event.method}\n\nevent.obj:\n{event.obj}\n\nevent.user_id:\n{event.user_id}
        \nevent.object:\n{event.object}""")
        return "ok"

@dp.my_signal_event_handle('дебагинфо', 'дебагинфа')
def about(event: MySignalEvent) -> str:
    if event.args == None:
        new_message(event.api, event.chat.peer_id,
        message=f"""Информация об объекте в распоряжении сервера:
        (добавь после команды цифру из списка)
        1. Сообщение(ответ или id с новой строки)

        Пока все, хули ты хотел?""")
        return "ok"
    elif event.args[0] == '1' or event.args[0] == 'сообщение':
        if event.payload:
            msgID = int(event.payload)
        else:
            msgID = event.reply_message['id']
        ret = event.api('messages.getById', message_ids = msgID)
        new_message(event.api, event.chat.peer_id, message = f'{ret}')
    return "ok"

@dp.my_signal_event_handle('отчет', 'репорт')
def report(event: MySignalEvent) -> str:
    IIS(event.payload)
    return "ok"