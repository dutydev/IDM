from duty.objects import dp, MySignalEvent
from html import escape
import re


@dp.longpoll_event_register('б')
@dp.my_signal_event_register('б')
def bomb(event: MySignalEvent):
    reply = ''
    sticker = ''
    data = False
    att = []
    text = ' '

    hours = re.findall(r'\d+ ?ч\w*', event.msg['text'])
    secs = re.findall(r'\d+ ?с\w*', event.msg['text'])
    mins = re.findall(r'\d+ ?м\w*', event.msg['text'])

    time = 0
    for i in hours:
        time += int(re.search(r'\d+', i)[0])*3600
    for i in mins:
        time += int(re.search(r'\d+', i)[0])*60
    for i in secs:
        time += int(re.search(r'\d+', i)[0])

    if time == 0:
        time = 60
    elif time > 86400:
        event.msg_op(2, '❗ Осади, максимальная длина - сутки')
        return "ok"
    t = time
    time = 15 if t <= 15 else 60 if t <= 60 else 900 if t <= 900 else 3600 if t <= 3600 else 86400
    event.msg_op(3)
    if event.payload:
        text = event.payload
        data = True

    if event.attachments:
        att.extend(event.attachments)
        data = True

    if event.reply_message:
        reply = event.reply_message['id']
        if event.reply_message['from_id'] == event.db.owner_id:
            atts = event.reply_message['attachments']
            if atts:
                atts = atts[0]
                if atts['type'] == 'sticker':
                    sticker = atts['sticker']
                    sticker = int(sticker['sticker_id'])
                    data = False
                    event.api.msg_op(3, msg_id=event.reply_message['id'])
                    reply = ''

    if not data:
        if event.reply_message:
            text = event.reply_message['text']
            reply = ''
        else:
            event.msg_op(2, '❗ Ну и че мне отправить?')
            return "ok"
    text = text.replace("\n", "<br>")
    event.api.exe('return API.messages.send({'+
        f'peer_id:{event.chat.peer_id},'+
        f'message:"{escape(text)}",'+
        f'expire_ttl:{time},'+
        f'attachment:"{",".join(att)}",'+
        f'sticker_id:"{sticker}",'+
        f'reply_to:"{reply}",'+
        'random_id:0'+
    '});', event.db.me_token)
    return "ok"
