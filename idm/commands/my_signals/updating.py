import os
import subprocess
from ...objects import dp, MySignalEvent
from ...lpcommands.utils import set_online_privacy, msg_op

path = os.getcwd()

@dp.my_signal_event_register('обновить')
def start_update(event: MySignalEvent):
    event.msg_op(2, '⏱ Начинаю процесс обновления...')
    ICAD = False
    for foldername in os.listdir():
        if foldername == "ICAD":
            ICAD = True
            break
    with open(os.path.join(path, "updater.py"), 'w', encoding="utf-8") as data:
        data.write(get_updater(ICAD, event.db.access_token, event.msg['id'], event.chat.peer_id))
    subprocess.Popen(f"python3 {path}/updater.py", shell=True)


def get_updater(ICAD: bool, token: str, message_id: int, peer_id: int):
    """import os
    import uwsgi
    import requests
    import subprocess
    folder = 'ICAD' if %s else 'IDM'
    def edit(text):
        requests.post(f'https://api.vk.com/method/messages.edit?v=5.100&lang=ru&access_token='+'%s',
                      data = {'message_id': %s, 'message': text, 'peer_id': %s}).json()
    commands = [
        f'cp -rf {folder}/database database',
        f'rm -rf {folder}',
        f'git clone https://github.com/elchinchel/{folder}',
        f'cp -rf database {folder}'
    ]
    fail = False
    for cmd in commands:
        if subprocess.run(cmd, shell=True).returncode != 0:
            fail = True
    uwsgi.reload()
    if fail:
        edit('Произошла какая-то беда, может обновилось, а может сдохло. На всякий случай помянем')
    else:
        edit('Как будто началось успешно, не дергай сервер полминутки...')
    """ %  (ICAD, token, message_id, peer_id)
