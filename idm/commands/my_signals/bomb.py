from ...objects import dp, MySignalEvent
from ...utils import edit_message, new_message, delete_message, sticker_message
from ...lp import execme

@dp.my_signal_event_handle('бомба', 'б')
def bomb(event: MySignalEvent) -> str:
    delete_message(event.api, event.chat.peer_id, event.msg['id'])
    reply = ''
    sticker = ''
    p = 0
    att = ''
    text = ' '
    if event.args:
        arg = ''
        try:
            time = int(event.args[0])
        except:
            arg =  event.args[0]
            time = int(arg[:-1])
            arg = arg[-1:]
        if len(event.args) == 2:
            arg = event.args[1]
        if arg == 'ч':
            time *= 3600
        if arg == 'м':
            time *= 60
        if time > 86400:
            new_message(event.api, event.chat.peer_id,
            message = 'Осади, максимальная длина - сутки', reply_to = event.msg['id'])
    else:
        new_message(event.api, event.chat.peer_id, message = '❗ Че по времени?')
        return "ok"
    if event.payload:
        text = event.payload
        p = 1
    if event.attachments:
        att = ",".join(event.attachments)
        p = 1
    if event.reply_message:
        reply = event.reply_message['id']
        if event.reply_message['from_id'] == event.user_id:
            atts = event.reply_message['attachments']
            if atts:
                atts = atts[0]
                if atts['type'] == 'sticker':
                    sticker = atts['sticker']
                    sticker = int(sticker['sticker_id'])
                    p = 1
                    reply = ''
                    delete_message(event.api, event.chat.peer_id, event.reply_message['id'])
    if p == 0:
        new_message(event.api, event.chat.peer_id, message = '❗ Ну и че мне отправить?')
        return "ok"
    code = """return API.messages.send({peer_id:%s,message:"%s",random_id:0,expire_ttl:%s,attachment:"%s",
    sticker_id:"%s",reply_to:"%s"});""" % (event.chat.peer_id, text, time, att, sticker, reply)
    execme(code = code)
    return "ok"