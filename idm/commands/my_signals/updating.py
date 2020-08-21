import os
import subprocess
from ...objects import dp, MySignalEvent
from ...lpcommands.utils import set_online_privacy, msg_op

try:
    import uwsgi
    updable = True
except ImportError:
    updable = False
    print('Обновление и анимации могут не работать')

path = os.path.join(os.getcwd(), 'ICAD')

@dp.my_signal_event_register('обновить')
def start_update(event: MySignalEvent):
    if not updable:
        event.msg_op(2, '❌ Недоступно')
        return "ok"
    event.msg_op(2, '⏱ Начинаю процесс обновления...')
    with open(os.path.join(path, "updater.py"), 'w', encoding="utf-8") as data:
        data.write(get_updater(event.db.access_token, event.msg['id'], event.chat.peer_id))
    subprocess.run(f"python3 {path}/updater.py", shell=True)
    uwsgi.reload()
    return "ok"


def get_updater(token: str, message_id: int, peer_id: int):
    return """
import os
import requests
import subprocess
def edit(text):
    requests.post(f'https://api.vk.com/method/messages.edit?v=5.100&lang=ru&access_token='+'%s',
                  data = {'message_id': %s, 'message': text, 'peer_id': %s}).json()
commands = [
    f'cd ICAD',
    'git fetch --all',
    'git reset --hard HEAD'
]
fail = False
for cmd in commands:
    if subprocess.run(cmd, shell=True).returncode != 0:
        fail = True
if fail:
    edit('Произошла какая-то беда, может обновилось, а может сдохло. На всякий случай помянем')
else:
    edit('Как будто началось успешно, не дергай сервер полминутки...')
    """ %  (token, message_id, peer_id)
