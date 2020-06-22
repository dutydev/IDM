#все еще 'unpythonic', ага, не ищи здесь нормальный код
from microvk import VkApi
from ..objects import DB, DB_general
from datetime import datetime
from time import sleep
import requests
import random
import re


class ExcReload(Exception):
    pass


def utils_api(db_ext: DB = None, api: VkApi = None):
    global db
    global vk
    db = db_ext
    vk = api

def parseByID(msg_id, atts = []):
    msg = (vk('messages.getById', message_ids = msg_id)['items'][0])
    return parse(msg, atts)

def parse(msg, atts = []):
    matches = re.findall(r'(\S+)|\n(.*)', msg['text'])
    del matches[0]
    cmd = matches.pop(0)[0].lower()
    args = []
    payload = ''
    for match in matches:
        if match[0]:
            args.append(match[0])
        else:
            payload += f'{match[1]}\n'
    if atts == 1:
        atts = att_parse(msg['attachments'])

    return {'args': args, 'payload': payload, 'command': cmd, 'attachments': atts,
            'reply': msg.get('reply_message'), "fwd": msg.get('fwd_messages')}

def att_parse(attachments):
    atts = []
    if attachments:
        for i in attachments:
            att_t = i['type']
            atts.append(att_t + str(i[att_t]['owner_id']) +
            '_' + str(i[att_t]['id']))
            if i[att_t].get('access_key'):
                atts[-1] += '_' + i[att_t]['access_key']
    return atts


def msg_op(mode: int, peer_id: str, message = '', msg_id = '', api = 0, delete: int = 0, **kwargs):
    #mode: 1 - отправка, 2 - редактирование, 3 - удаление, 4 - удаления только для себя
    if not api: api = vk
    if 2000000000 > peer_id > 1000000000:
        peer_id = ~peer_id + 1000000001

    if mode == 4:
        mode = 3
        dfa = 0
    else: dfa = 1

    mode = ['messages.send', 'messages.edit', 'messages.delete'][mode - 1]
    response = api(mode, peer_id = peer_id, message = message,
    message_id = msg_id, delete_for_all = dfa, random_id = 0, **kwargs)
    if delete:
        sleep(delete)
        api('messages.delete', message_id = msg_id, delete_for_all = 1)
    return response


def get_msgs(peer_id, offset = 0):
    return exe('''return (API.messages.getHistory({"peer_id":"%s",
    "count":"200", "offset":"%s"}).items) + (API.messages.getHistory({"peer_id":
    "%s", "count":"200", "offset":"%s"}).items);''' %
    (peer_id, offset, peer_id, offset + 200))

def get_last_th_msgs(peer_id):
    return exe('''return (API.messages.getHistory({"peer_id":"%(peer)s",
    "count":"200", "offset":0}).items) + (API.messages.getHistory({"peer_id":
    "%(peer)s", "count":"200", "offset":200}).items) + (API.messages.getHistory({"peer_id":
    "%(peer)s", "count":"200", "offset":400}).items) + (API.messages.getHistory({"peer_id":
    "%(peer)s", "count":"200", "offset":600}).items) + (API.messages.getHistory({"peer_id":
    "%(peer)s", "count":"200", "offset":800}).items);''' % {'peer': peer_id})
    


def MSI(message: str):
    msg_op(1, db.duty_id, message)

def send_info(message: str):
    msg_op(1, -195759899, message)

def exe(code):
    'Метод execute'
    return vk('execute', code = code)


def get_msg(api, peer_id, local_id):
    try:
        data = api("messages.getByConversationMessageId",
            peer_id = peer_id, conversation_message_ids = local_id)
        return data['items'][0]
    except:
        return None


def timenow():
    return datetime.now().timestamp()


def user_info(user_id = ''):
    return vk('users.get', user_ids = user_id)[0]


def execme(code: str) -> int:
    if db.me_token == '':
        return "-1"
    vk = VkApi(access_token = db.me_token)
    return vk('execute', code = code)


def gen_secret(chars = 'abcdefghijklmnopqrstuvwxyz0123456789_-'):
    secret = ''
    length = random.randint(64, 80)
    while len(secret) < length:
        secret += chars[random.randint(0, 37)]
    return secret


def find_user_mention(text):
    uid = re.search(r'\[id\d*\|', text)
    if uid: uid = int(uid[0][3:-1])
    return uid

def find_mention_by_message(msg):
    user_id = None
    if msg['args']:
        user_id = find_user_mention(msg['args'][0])
    elif msg['reply']:
        user_id = msg['reply']['from_id']
    return user_id

def set_online_privacy(db, mode = 'only_me'):
    url = ('https://api.vk.me/method/account.setPrivacy?v=5.109&key=online&value=%s&access_token=%s'
    % (mode, db.me_token))
    r = requests.get(url, headers = {"user-agent": "VKAndroidApp/1.123-123 (Android 123; SDK 123; IDM-SC-mod; 1; ru; 123x123)"}).json()
    if r['response']['category'] == mode:
        return True
    else:
        return False