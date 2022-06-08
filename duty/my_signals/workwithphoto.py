from duty.objects import MySignalEvent, dp
import requests, os
# Не спиздил, а позаимствовал


@dp.longpoll_event_register('негатив')
@dp.my_signal_event_register('негатив')
def nigga(event: MySignalEvent) -> str:
    if not (event.attachments or event.reply_message):
            event.msg_op(2, "❗ Нет данных")
            return "ok"

    if event.reply_message:
        event.attachments = event.reply_message['attachments']
        if event.attachments:
            if event.attachments[0]['type'] != 'photo':
                event.msg_op(2, 'Как я тебе не на картинку наложу фильтр?')
                return "ok"
            url = event.attachments[0]['photo']['sizes'][-1]['url']
    else:
        if event.msg['attachments'][0]['type'] != 'photo':
            event.msg_op(2, 'Как я тебе не на картинку наложу фильтр?')
            return "ok"
        url = event.msg['attachments'][0]['photo']['sizes'][-1]['url']
    r = requests.get(url)
    filename = os.path.join(os.getcwd(), 'file.png')
    out = open(filename, "wb")
    out.write(r.content)
    out.close()

    os.system(f"convert {filename} -negate {filename}")

    upload_url = event.api('photos.getMessagesUploadServer')['upload_url']
    uploaded = requests.post(upload_url, files={'photo': open(filename, 'rb')}).json()
    a = event.api('photos.saveMessagesPhoto', server=uploaded["server"], photo=uploaded["photo"], hash=uploaded["hash"])[0]
    event.msg_op(2, '', attachment=f'photo{a["owner_id"]}_{a["id"]}')
    os.remove(filename)
    return "ok"


@dp.longpoll_event_register('жмых')
@dp.my_signal_event_register('жмых')
def dist(event: MySignalEvent) -> str:
    if not (event.attachments or event.reply_message):
            event.msg_op(2, "❗ Нет данных")
            return "ok"

    if event.reply_message:
        event.attachments = event.reply_message['attachments']
        if event.attachments:
            if event.attachments[0]['type'] != 'photo':
                event.msg_op(2, 'Как я тебе не на картинку наложу фильтр?')
                return "ok"
            url = event.attachments[0]['photo']['sizes'][-1]['url']
            hw = str(event.attachments[0]['photo']['sizes'][-1]['height'])+'x'+str(event.attachments[0]['photo']['sizes'][-1]['width'])
    else:
        if event.msg['attachments'][0]['type'] != 'photo':
            event.msg_op(2, 'Как я тебе не на картинку наложу фильтр?')
            return "ok"
        url = event.msg['attachments'][0]['photo']['sizes'][-1]['url']
        hw = str(event.attachments[0]['photo']['sizes'][-1]['height'])+'x'+str(event.attachments[0]['photo']['sizes'][-1]['width'])
    r = requests.get(url)
    filename = os.path.join(os.getcwd(), 'file.png')
    out = open(filename, "wb")
    out.write(r.content)
    out.close()
    prefer_size = event.msg['text'].split()[-1]
    if prefer_size.isnumeric():
        prefer_size = int(prefer_size)
        if prefer_size <= 10 and prefer_size >= 1:
            believe_size = 50 - 5*(prefer_size-1)
            size = f'{believe_size}x{believe_size}%'
        else:
            event.msg_op(2, 'Степень жмыха от 1 до 10')
    else:
        size = '50x50%'

    os.system(f"convert {filename} -liquid-rescale {size} -resize {hw} {filename}")

    upload_url = event.api('photos.getMessagesUploadServer')['upload_url']
    uploaded = requests.post(upload_url, files={'photo': open(filename, 'rb')}).json()
    a = event.api('photos.saveMessagesPhoto', server=uploaded["server"], photo=uploaded["photo"], hash=uploaded["hash"])[0]
    event.msg_op(2, '', attachment=f'photo{a["owner_id"]}_{a["id"]}')
    os.remove(filename)
    return "ok"

