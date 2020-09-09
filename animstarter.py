import os
import json
import subprocess
from platform import system

cwd = os.getcwd()

already_in = False
for name in os.listdir(cwd):
    if name == 'animplayer.py':
        already_in = True

path = cwd if already_in else os.path.join(cwd, 'ICAD')
runner = 'python3' if system() == 'Linux' else 'py'

def start_player(peer, msg_id, token, pics, delay, play_list):
    animdata = {
        "peer": peer,
        "msg_id": msg_id,
        "token": token,
        "delay": delay,
        "pics": pics,
        "play_list": play_list
    }
    with open(os.path.join(cwd, "animdata"), 'w', encoding="utf-8") as data:
        data.write(json.dumps(animdata, ensure_ascii=False))
    subprocess.Popen(f"{runner} {path}/animplayer.py", shell=True)
