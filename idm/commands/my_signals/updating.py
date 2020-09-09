import os
import subprocess
from platform import system
from idm.objects import dp, MySignalEvent

# try:
#     import uwsgi
#     PA = True
# except ImportError:
#     PA = False
#     print('Обновление и анимации могут не работать')

cwd = os.getcwd()

already_in = False
for name in os.listdir(cwd):
    if name == 'animplayer.py':
        already_in = True

path = cwd if already_in else os.path.join(cwd, 'ICAD')
runner = 'python3' if system() == 'Linux' else 'py'

@dp.my_signal_event_register('обновить')
def start_update(event: MySignalEvent):
    event.msg_op(2, '⏱ Начинаю процесс обновления...' if PA else
                    '\nРабота не на pythonanywhere не гарантируется')
    with open(os.path.join(path, "updater.py"), 'w', encoding="utf-8") as data:
        data.write(get_updater(event.db.access_token, event.msg['id'], event.chat.peer_id))
    out = subprocess.run(f"{runner} {path}/updater.py", shell=True, cwd=path, capture_output=True)
    with open(os.path.join(os.getcwd(), "update.log"), 'w', encoding="utf-8") as data:
        data.write(str(out))
    if PA:
        uwsgi.reload()
    return "ok"


def get_updater(token: str, message_id: int, peer_id: int):
    if PA:
        msg = '✅ Ок, не трогай сервер секунд пять...'
    else:
        msg = '✅ Перезапусти скрипт'
    return """
import os
import requests
import subprocess
def edit(text):
    requests.post(f'https://api.vk.com/method/messages.edit?v=5.100&lang=ru&access_token='+'%s',
                  data = {'message_id': %s, 'message': text, 'peer_id': %s})
commands = [
    'git fetch --all',
    'git reset --hard origin/master-beta'
]
fail = False
for cmd in commands:
    if subprocess.run(cmd, shell=True).returncode != 0:
        fail = True
if fail:
    edit('❌ Помянем (скинь update.log из рабочей директории)')
else:
    edit('%s')
    """ %  (token, message_id, peer_id, msg)
