from ...objects import dp
from ...lpcommands.utils import set_online_privacy, msg_op
from ...sync import sync_send

not_installed = '❗ LP модуль не установлен\nСсылка на инструкцию по установке есть на сайте в разделе "Настройка LP модуля"'

@dp.my_signal_event_register('+онлайн', '-онлайн')
def online(event):
    if event.db.lp['installed']:
        s = event.db.settings
        if event.command.startswith('+'):
            if s['offline']:
                msg = '❗ Сначала отключите оффлайн'
            else:
                s['online'] = True
        else:
            s['online'] = False
        db.lp['unsynced_changes'].update({'settings': event.db.settings})
        event.db.save()
        msg_op(1, -195759899, '!syncchanges')
    else:
        msg = not_installed
    msg_op(2, event.chat.peer_id, msg, event.msg['id'])
    return "ok"




@dp.my_signal_event_register('+оффлайн', '-оффлайн')
def offline(event):
    if event.db.lp['installed']:
        s = event.db.settings
        if event.command.startswith('+'):
            s['offline'] = True
            set_online_privacy(event.db)
            s['online'] = False
        else:
            set_online_privacy(event.db, 'all')
            s['offline'] = False
        db.lp['unsynced_changes'].update({'settings': event.db.settings})
        event.db.save()
        msg_op(1, -195759899, '!syncchanges')
    else:
        msg = not_installed
    msg_op(2, event.chat.peer_id, msg, event.msg['id'])
    return "ok"
