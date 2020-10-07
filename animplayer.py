import os
import json
import time
import requests

path = os.getcwd()
filepath = os.path.join(path, "animdata")

with open(filepath, 'r', encoding="utf-8") as data:
    animdata = json.loads(data.read())
os.remove(filepath)

request_data = {
    "peer_id": animdata["peer"],
    "message_id": animdata["msg_id"]
}


def edit(text):
    request_data.update({"message": text})
    r = requests.post('https://api.vk.com/method/messages.edit?'+
                      'v=5.100&lang=ru&keep_forward_messages=1' +
                      '&access_token=' + animdata["token"],
                      data=request_data).json()
    if 'error' in r:
        raise Exception(r['error']['error_msg'])


pics = animdata["pics"]

if animdata['play_list']:
    for i in range(len(pics)):
        edit(pics[i])
        time.sleep(animdata["delay"])
else:
    for _ in range(len(pics[0]) + 1):
        edit('\n'.join(pics))
        for i in range(len(pics)):
            pics[i] = pics[i][-1:] + pics[i][:-1]
        time.sleep(animdata["delay"])
