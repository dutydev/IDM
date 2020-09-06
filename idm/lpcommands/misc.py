from .utils import msg_op, user_info, MSI, get_last_th_msgs
from ..objects import DB
from . import dlp, ND
from datetime import datetime
from microvk import VkApiResponseException
import time, re



@dlp.register('пуши', 'уведы')
def mention_search(nd):
    mention = f'[id{nd.db.duty_id}|'
    msg_ids = []

    for msg in get_last_th_msgs(nd[3]):
        if nd.time - msg['date'] >= 86400: break
        if mention in msg['text']:
            msg_ids.append(str(msg['id']))
    
    if not msg_ids: msg = 'Ничего не нашел 😟'
    else: msg = 'Собсна, вот что нашел за последние 24 часа:'

    msg_op(1, nd[3], msg, forward_messages = ','.join(msg_ids))
    return "ok"


@dlp.register_startswith('ксмс')
def tosms(nd):
    if nd[3] < 2000000000:
        msg_op(2, nd[3], '❗ Не работает в ЛС', msg_id = nd[1])
        return "ok"
    msg = (nd.vk('messages.getByConversationMessageId', peer_id = nd[3],
        conversation_message_ids = re.search(r'\d+', nd[5])[0])['items'])
    if msg:
        if msg[0].get('action'): (msg_op(2, nd[3],
            'Это сообщение - действие, не могу переслать', msg_id = nd[1]))
        else: msg_op(1, nd[3], 'Вот ента:', forward_messages = msg[0]['id'])
    else:
        msg_op(2, nd[3],'❗ ВК вернул пустой ответ', msg_id = nd[1])
    return "ok"


def booo(nd):
    h = m = s = 0
    nd[5] = nd[5].replace('пип', '')
    hours = re.findall(r'\d+ ?ч\w*', nd[5])
    secs = re.findall(r'\d+ ?с\w*', nd[5])
    mins = re.findall(r'\d+ ?м\w*', nd[5])

    for i in hours:
        h += int(re.search(r'\d+', i)[0])
    for i in mins:
        m += int(re.search(r'\d+',i)[0])
    for i in secs:
        s += int(re.search(r'\d+',i)[0])

    
    msg_op(1, nd[3], f'H: {h}, M: {m}, S:{s}')

