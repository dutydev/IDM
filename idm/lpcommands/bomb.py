from .utils import execme, msg_op
from ..objects import DB
import re


def bomb(nd, db, vk, msg = 0):
    if not msg:
        msg = (vk('messages.getById', message_ids = nd[1])['items'][0])
    msg_op(3, nd[3], msg_id = nd[1])
    reply = ''
    sticker = ''
    p = 0
    att = []
    text = ' '

    payload = ''.join(re.findall(r'\n.*', msg['text']))

    hours = re.findall(r'\d+ ?ч\w*', nd[5])
    secs = re.findall(r'\d+ ?с\w*', nd[5])
    mins = re.findall(r'\d+ ?м\w*', nd[5])

    time = 0
    for i in hours:
        time += int(re.search(r'\d+', i)[0])*3600
    for i in mins:
        time += int(re.search(r'\d+',i)[0])*60
    for i in secs:
        time += int(re.search(r'\d+',i)[0])
    
    if not time: time = 60
    elif time > 86400:
        msg_op(1, nd[3], '❗ Осади, максимальная длина - сутки')
        return "ok"

    if payload:
        text = payload
        p = 1

    if msg['attachments']:
        for i in msg['attachments']:
            att_t = i['type']
            att.append(att_t + str(i[att_t]['owner_id']) +
            '_' + str(i[att_t]['id']))
            p = 1

    if 'reply_message' in msg:
        reply = msg['reply_message']['id']
        if msg['reply_message']['from_id'] == db.duty_id:
            atts = msg['reply_message']['attachments']
            if atts:
                atts = atts[0]
                if atts['type'] == 'sticker':
                    sticker = atts['sticker']
                    sticker = int(sticker['sticker_id'])
                    p = 1
                    msg_op(3, nd[3], msg_id = reply)
                    reply = ''

    if p == 0:
        if reply:
            text = msg['reply_message']['text']
            reply = ''
        else:
            msg_op(1, nd[3], '❗ Ну и че мне отправить?')
            return
    code = """return API.messages.send({peer_id:%s,message:"%s",random_id:0,expire_ttl:"%s",attachment:"%s",
    sticker_id:"%s",reply_to:"%s"});""" % (nd[3], text[1:], time, ",".join(att), sticker, reply)
    execme(code = code)
    return "ok"