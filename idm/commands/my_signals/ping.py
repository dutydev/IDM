from ...objects import dp, MySignalEvent
from ...utils import edit_message, new_message, delete_message, sticker_message
from datetime import datetime, date
import socket, time
import vkapi
from ...pythonping import ping as pingp

@dp.my_signal_event_handle('пинг', 'пиу', 'кинг', 'п', 'пингб', 'тик')
def ping(event: MySignalEvent) -> str:

    if event.command == 'пингб':
        new_message(event.api, event.chat.peer_id, message='PONG')
        return "ok"
    c_time = datetime.now().timestamp()
    delta = round(c_time - event.msg['date'], 3)

    #c_time_str = str(datetime.fromtimestamp(round(c_time)))
    #v_time_str = str(datetime.fromtimestamp(round(event.msg['date'])))

    r_type = 'ПОНГ' if event.command == "пинг" else "ПАУ" if event.command == "пиу" else "ТОК" if event.command == "тик" else "КОНГ"

    if delta > 15:r_type += "\nМОРОСИТ КОНКРЕТНО КТО-ТО!!!!!"
    elif delta > 10:r_type += "\nЭЭЭЭЭ КТО МОРОСИТ?!"
    elif delta > 5:r_type += "\nМоросит кто-то, что ли?"
    else:r_type += "\nЕжжи по каефу работает всё"

    message = f"""{r_type}

    Время ответа: {delta} с.
    """.replace('    ', '')
    new_message(event.api, event.chat.peer_id, message=message)
    return "ok"

# пинг сайтов не работает без прав администратора / суперпользователя
# пример команды:
# .с пс ya ru
@dp.my_signal_event_handle('пингс', 'пс')
def pings(event: MySignalEvent) -> str:
    site = ".".join(event.args)
    if event.db.host.find('pythonanywhere') != -1 and event.payload != 'игнор':
        new_message(event.api, event.chat.peer_id,
        message=f"""❌ Пинг сайтов не работает на pythonanywhere ❌ \n
        Вообще, откровенно говоря, я не знаю, будет ли это работать
        на каком-либо другом хостинге, но в идеальных условиях,
        когда дежурный запущен с правами админа или su, оно работать должно""")
        return "ok"
    try:
        ip = socket.gethostbyname(site)
    except:
        new_message(event.api, event.chat.peer_id, message=f'❗ Ресурс неизвестен')
        return "ok"
    resp = 'null'
    resp = pingp(ip, size=128, count=1)
    try:
        for i in 0, 1, 2, 3:
            msg = 'Пингую...'
            resp = pingp(ip, size=128, count=1)
            msg = msg + '\n' + resp
            edit_message(event.api, event.chat.peer_id, event.msg['id'], message=msg)
            time.sleep(1)
    except:
        new_message(event.api, event.chat.peer_id, message=f'❗ Пинг проебался')

    new_message(event.api, event.chat.peer_id, message=f'ip = {ip}\nsite = {site}')

    return "ok"




