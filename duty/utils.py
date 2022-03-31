import os
import re
import sys
import random
from typing import Any, Iterable, Union, List, TypeVar
from microvk import VkApi, VkApiResponseException


MySignalEvent = TypeVar("MySignalEvent")
cmid_key = 'conversation_message_id'

dirname = os.path.dirname
joinpath = os.path.join

ROOT_DIR = dirname(dirname(os.path.abspath(__file__)))


def path_from_root(*paths) -> str:
    return joinpath(ROOT_DIR, *paths)


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


def format_response(text: str, **values):
    for key in values.keys():
        if not key.islower():
            values[key.lower()] = values.pop(key)
    for var_name in re.findall(r'{([^} ]+)}', text):
        if (lowcase := var_name.lower()) not in values:
            values[lowcase] = (
                f'{{Ошибка! Не существует переменной "{var_name}", '
                'ВНИМАТЕЛЬНО проверь название}'
            )
        text = text.replace('{'+var_name+'}', str(values[lowcase]))
    return text


class Message:
    text: str
    args: List[str]
    payload: str
    command: str
    attachments: List[str]
    reply: dict
    fwd: List[dict]

    def __init__(self, msg: dict):
        matches = re.findall(r'(\S+)|\n(.*)', msg['text'])
        del matches[0]
        if matches != []:
            self.command = matches.pop(0)[0].lower()
        else:
            self.command = ''
        self.reply = msg.get('reply_message', {})
        self.fwd = msg.get('fwd_messages', [])
        self.text = msg['text']
        self.payload = ''
        self.args = []
        for i, match in enumerate(matches, 1):
            if match[0]:
                self.args.append(match[0])
            else:
                self.payload += match[1] + ('\n' if i < len(matches) else '')
        self.attachments = att_parse(msg['attachments'])


def gen_secret(chars='abcdefghijklmnopqrstuvwxyz0123456789',
               length: int = None):
    secret = ''
    length = length or random.randint(64, 80)
    while len(secret) < length:
        secret += chars[random.randint(0, len(chars)-1)]
    return secret


def find_user_mention(text: str) -> Union[int, None]:
    uid = re.findall(r'\[(id|public|club)(\d*)\|', text)
    if uid:
        if uid[0][0] != 'id':
            uid = 0 - int(uid[0][1])
        else:
            uid = int(uid[0][1])
    return uid


def find_user_by_link(text: str, vk: VkApi) -> Union[int, None]:
    user = re.findall(r"vk.com\/(id\d*|[^ \n]*\b)", text)
    if user:
        try:
            return vk('users.get', user_ids=user)[0]['id']
        except (VkApiResponseException, IndexError):
            return None


def get_index(item: Iterable, index: int, default: Any = None):
    try:
        return item[index]
    except IndexError:
        return default


def find_mention_by_event(event: MySignalEvent) -> Union[int, None]:
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


def format_push(u: dict) -> str:
    uid = u['id']
    if u.get('first_name') is None:
        return f"[club{abs(uid)}|{u['name']}]"
    else:
        return f"[id{uid}|{u['first_name']} {u['last_name']}]"


def ment_user(user: dict) -> str:
    return format_push(user)


def get_plural(number: Union[int, float], one: str, few: str,
               many: str, other: str = '') -> str:
    """`one`  = 1, 21, 31, 41, 51, 61...\n
    `few`  = 2-4, 22-24, 32-34...\n
    `many` = 0, 5-20, 25-30, 35-40...\n
    `other` = 1.31, 2.31, 5.31..."""
    if type(number) == float:
        if not number.is_integer():
            return other
        else:
            number = int(number)
    if number % 10 in {2, 3, 4}:
        if not 10 < number < 20:
            return few
    number = str(number)
    if number[-1] == '1':
        return one
    return many
