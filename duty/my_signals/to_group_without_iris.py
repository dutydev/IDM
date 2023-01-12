from duty.objects import MySignalEvent, dp
import requests
import re
from duty.api_utils import get_msg
import time
from io import BytesIO
from datetime import datetime, timezone, timedelta
import typing
from duty.utils import cmid_key, find_user_mention
from microvk import VkApi, VkApiResponseException


def upload_photo(event: MySignalEvent, url: str) -> str:
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


def parse_message(event: MySignalEvent, payload: str) -> typing.Tuple[str, typing.List[str]]:
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
    event.set_msg()
    for att in event.msg.get('attachments', []):
            atype = att['type']
            if atype in ['link']:
                continue
            if atype == 'photo':
                attachments.append(upload_photo(event, att['photo']['sizes'][-1]['url']))
            else:
                attachments.append(
                    f"{atype}{att[atype]['owner_id']}_{att[atype]['id']}_{att[atype]['access_key']}"
                )
    return payload, attachments


def get_usernames(event: MySignalEvent, ids):
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


def find_user_by_link(text: str, vk: VkApi) -> typing.Union[int, None]:
    user = re.findall(r"vk.com\/(club\d*|[^ \n]*\b)", text)
    if user is []:
        user = re.findall(r"vk.com\/(public\d*|[^ \n]*\b)", text)
    if user:
        try:
            return vk('groups.getById', group_ids=user)[0]['id']
        except (VkApiResponseException, IndexError):
            return None


def get_group_id(event: MySignalEvent) -> typing.Union[int, None]:
    user_id = None
    if event.args:
        user_id = find_user_mention(event.args[0])
    if event.reply_message and not user_id:
        user_id = event.reply_message['from_id']
    if not user_id:
        user_id = find_user_by_link(event.msg['text'], event.api)
        if user_id is not None:
            user_id = -user_id
    if event.msg['fwd_messages'] and not user_id:
        user_id = event.msg['fwd_messages'][0]['from_id']
    return user_id


@dp.longpoll_event_register('вгр')
@dp.my_signal_event_register('вгр')
def vgr(event: MySignalEvent) -> str:
    event.set_msg()
    arg_line, _, payload = event.msg['text'].partition('\n')
    args = arg_line.split()
    group_id = get_group_id(event)

    if group_id is None:
        group_id = event.db.to_group_saved_group_id
    elif group_id < 0:
        event.db.to_group_saved_group_id = group_id

    if group_id is None:
        event.send('⚠️ Не указана группа, в которую нужно сделать пост!')
        return 'ok'

    if group_id > 0:
        event.send('⚠️ Нужна ссылочка на группу, а не пользователя.')
        return 'ok'

    event.obj.update({'group_id': abs(group_id)})
    send = lambda *a, **kw: MySignalEvent.send(event, *a, **kw)
    if 'через' in arg_line:
        delay = get_delay(arg_line)
    else:
        delay = 0
    if 'диалог' in arg_line:
        if not event.msg['fwd_messages']:
            send('Диалог кого с кем?')
            return "ok"
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
    try:
        publish_date = datetime.now(timezone(timedelta(hours=3))).timestamp() + delay
        params = {
            'owner_id': group_id,
            'from_group': 1,
            'message': text,
            'attachments': ",".join(attachments)
        }

        if delay != 0:
            params['publish_date'] = publish_date

        try:
            data = event.api('wall.post', **params)
        except VkApiResponseException as e:
            if 'user should be group editor' in str({e.error_msg}).lower():
                params['from_group'] = 0
                data = event.api('wall.post', **params)
            else:
                raise

        if delay == 0:
            send(event.responses['to_group_success'],
                 attachment=f"wall{group_id}_{data['post_id']}")
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
