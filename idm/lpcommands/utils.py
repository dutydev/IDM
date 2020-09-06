#все еще 'unpythonic', ага, не ищи здесь нормальный код
from microvk import VkApi
from ..objects import DB, DB_general
from datetime import datetime
from typing import Union
from time import sleep
import requests
import random
import re


vk: VkApi
db: DB


def utils_api(db_ext: DB = None, api: VkApi = None):
    global db
    global vk
    db = db_ext
    vk = api

def parseByID(msg_id, atts: bool = False):
    msg = (vk('messages.getById', message_ids = msg_id)['items'][0])
    return parse(msg, atts)

def parse(msg, atts: bool = False):
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
    if atts:
        atts = att_parse(msg['attachments'])

    return {'text': msg['text'], 'args': args, 'payload': payload, 'command': cmd, 'attachments': atts or [],
            'reply': msg.get('reply_message'), "fwd": msg.get('fwd_messages')}

def att_parse(attachments):
    atts = []
    if attachments:
        for i in attachments:
            att_t = i['type']
            if att_t in {'link', 'article'}: continue
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


def gen_secret(chars = 'abcdefghijklmnopqrstuvwxyz0123456789', length: int = None):
    secret = ''
    length = length or random.randint(64, 80)
    while len(secret) < length:
        secret += chars[random.randint(0, len(chars)-1)]
    return secret


def find_user_mention(text):
    uid = re.findall(r'\[(id|public|club)(\d*)\|', text)
    if uid:
        if uid[0][0] != 'id':
            uid = 0 - int(uid[0][1])
        else:
            uid = int(uid[0][1])
    return uid

def find_user_by_link(text, vk):
    user = re.findall(r"vk.com\/(id\d*|[^ \n]*\b)", text)
    if user:
        try:
            return vk('users.get', user_ids = user)[0]['id']
        except:
            pass

def find_mention_by_message(msg: dict, vk: VkApi) -> Union[int, None]:
    'Возвращает ID пользователя, если он есть в сообщении, иначе None'
    user_id = None
    if msg['args']:
        user_id = find_user_mention(msg['args'][0])
    if msg['reply'] and not user_id:
        user_id = msg['reply']['from_id']
    if not user_id:
        user_id = find_user_by_link(msg['text'], vk)
    if msg['fwd'] and not user_id:
        user_id = msg['fwd'][0]['from_id']
    print(f'UID: {user_id}' if user_id else 'UID not found!')
    return user_id

def find_mention_by_event(event: "MySignalEvent") -> Union[int, None]:
    'Возвращает ID пользователя, если он есть в сообщении, иначе None'
    user_id = None
    if event.args:
        user_id = find_user_mention(event.args[0])
    if event.reply_message and not user_id:
        user_id = event.reply_message['from_id']
    if not user_id:
        user_id = find_user_by_link(event.msg['text'], event.api)
    if event.msg['fwd_messages'] and not user_id:
        user_id = event.msg['fwd_messages'][0]['from_id']
    return user_id


def set_online_privacy(db, mode = 'only_me'):
    url = ('https://api.vk.me/method/account.setPrivacy?v=5.109&key=online&value=%s&access_token=%s'
    % (mode, db.me_token))
    r = requests.get(url, headers = {"user-agent": "VKAndroidApp/1.123-123 (Android 123; SDK 123; IDM-SC-mod; 1; ru; 123x123)"}).json()
    if r['response']['category'] == mode:
        return True
    else:
        return False