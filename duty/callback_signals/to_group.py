# TODO: навести красоту
import typing
from duty.api_utils import get_msg
from duty.objects import dp, Event, SignalEvent
from duty.utils import cmid_key
from microvk import VkApiResponseException
import re
import time
import requests
from io import BytesIO
from datetime import datetime, timezone, timedelta


def upload_photo(event: Event, url: str) -> str:
    time.sleep(0.6)
    server = event.api("photos.getWallUploadServer", group_id=event.obj['group_id'])
    im = BytesIO()
    im.write(requests.get(url).content)
    im.seek(0)
    im.name = 'ph.jpeg'
    data = requests.post(server['upload_url'], files={'photo': im}).json()
    print(data)
    attach = event.api("photos.saveWallPhoto", group_id=event.obj['group_id'], **data)[0]
    return f"photo{attach['owner_id']}_{attach['id']}_{attach['access_key']}"


def parse_message(event: SignalEvent, payload: str) -> typing.Tuple[str, typing.List[str]]:
    attachments = []
    if event.reply_message is not None:
        if payload == "":
            payload = event.reply_message['text']
        time.sleep(0.3)
        message = get_msg(event.api, event.chat.peer_id, event.reply_message[cmid_key])
        for att in message.get('attachments', []):
            atype = att['type']
            if atype in ['link']:
                continue
            if atype == 'photo':
                max_size = max(att['photo']['sizes'], key=lambda s: s['width'] + s['height'])
                attachments.append(upload_photo(event, max_size['url']))
            else:
                attachments.append(
                    f"{atype}{att[atype]['owner_id']}_{att[atype]['id']}_{att[atype]['access_key']}"
                )
    attachments.extend(event.attachments)
    return payload, attachments


def get_usernames(event: Event, ids):
    users = {}
    for user in event.api('users.get', user_ids=','.join([str(i) for i in ids])):
        users[user['id']] = f'[id{user["id"]}|{user["first_name"]} {user["last_name"]}]'
    return users


def get_delay(text):
    multipliers = {
        "мес": 2592000,
        "н": 604800,
        "д": 86400,
        "ч": 3600,
        "м": 60,
        "с": 1
    }
    regexp = r'(\d+) ?(мес|д|н|ч|с|м)\w*'
    delay = 0
    for count, period in re.findall(regexp, text):
        delay += int(count) * multipliers[period]
    return delay


@dp.event_register('toGroup')
def to_group(event: Event) -> str:
    event.set_msg()
    arg_line, _, payload = event.msg['text'].partition('\n')
    args = arg_line.split()
    if 'через' in arg_line:
        delay = get_delay(arg_line)
    else:
        delay = 0
    if 'диалог' in arg_line:
        if not event.msg['fwd_messages']:
            return send('Диалог кого с кем?')
        user_ids = set()
        for msg in event.msg['fwd_messages']:
            user_ids.add(msg['from_id'])
        unames = get_usernames(event, user_ids)
        text = payload + '\n\n' if payload else ''
        for msg in event.msg['fwd_messages']:
            text += f'{unames[msg["from_id"]]}: {msg["text"]}\n'
        attachments = event.attachments
    else:
        text, attachments = parse_message(event, payload)
        if 'автор' in arg_line:
            if event.reply_message:
                uname = get_usernames(event, [event.reply_message['from_id']]).popitem()[1]
            else:
                uname = get_usernames(event, [event.db.owner_id]).popitem()[1]
            text = f'Автор: {uname}\n{text}'
    send = lambda *a, **kw: SignalEvent.send(event, *a, **kw)
    try:
        publish_date = datetime.now(timezone(timedelta(hours=3))).timestamp() + delay
        params = {
            'owner_id': 0-event.obj['group_id'],
            'from_group': 1,
            'message': text,
            'attachments': ",".join(attachments)
        }
        if delay != 0:
            params['publish_date'] = publish_date
        data = event.api('wall.post', **params)
        if delay == 0:
            send(event.responses['to_group_success'],
                      attachment=f"wall-{event.obj['group_id']}_{data['post_id']}")
        else:
            date = datetime.fromtimestamp(publish_date)
            send(f'Запись будет опубликована\n{date.ctime()}') # TODO: формат для тупых и отсталых
    except VkApiResponseException as e:
        if e.error_code == 214:
            send(event.responses['to_group_err_forbidden'])
        elif e.error_code == 220:
            send(event.responses['to_group_err_recs'])
        elif e.error_code == 222:
            send(event.responses['to_group_err_link'])
        else:
            send(event.responses['to_group_err_vk'] + str({e.error_msg}))
    #except Exception as e:
       # send(event.responses['to_group_err_unknown'])
    return "ok"
