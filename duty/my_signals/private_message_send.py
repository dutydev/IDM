from datetime import datetime
from time import sleep
from duty.utils import find_mention_by_event
from microvk import VkApiResponseException
from duty.objects import MySignalEvent, dp


@dp.longpoll_event_register('в', 'влс')
@dp.my_signal_event_register('в', 'влс')
def send_private(event: MySignalEvent) -> str:
    def abort(text):
        event.msg_op(2, text)
        return "ok"
    if event.command == 'в':
        if event.args[0] != 'лс':
            return "ok"
    uid = find_mention_by_event(event)
    if uid:
        if not (event.payload or event.attachments):
            if event.args and event.reply_message:
                if event.args[0] == 'лс' and len(event.args == 1):
                    abort('❗ Нет данных')
                else:
                    event.payload = ' '.join(event.args)
            else:
                abort('❗ Нет данных')
        try:
            event.api.msg_op(1, uid, event.payload, attachment = ','.join(event.attachments))
            msg = '✅ Сообщение отправлено'
        except VkApiResponseException as e:
            if e.error_code == 902:
                msg = '❗ Пользователь ограничил круг лиц, которые могут отправлять ему сообщения'
            else:
                msg = f'❗ Ошибка VK №{e.error_code}: {e.error_msg}'
        event.msg_op(2, msg)
    else:
        event.msg_op(2, '❗ Необходимо упоминание или ответ на сообщение')
    return "ok"
