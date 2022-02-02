import os
import requests

from PIL import Image
from duty.objects import dp, MySignalEvent


@dp.longpoll_event_register('сперм', 'sperm')
@dp.my_signal_event_register('сперм', 'sperm')
def cum(event: MySignalEvent) -> str:
    if not (event.attachments or event.reply_message):
        event.msg_op(2, "❗ Нет данных")
        return "ok"

    if event.reply_message:
        event.attachments = event.reply_message['attachments']
        if event.attachments:
            if event.attachments[0]['type'] != 'photo':
                event.msg_op(2, 'Как я тебе не из картинки сделаю картинОчку?')
                return "ok"
            url = event.attachments[0]['photo']['sizes'][-1]['url']
    else:
        if event.msg['attachments'][0]['type'] != 'photo':
            event.msg_op(2, 'Как я тебе не из картинки сделаю картинОчку?')
            return "ok"
        url = event.msg['attachments'][0]['photo']['sizes'][-1]['url']

    r = requests.get(url)
    out = open('content/input.png', "wb")
    out.write(r.content)
    out.close()
    fon = Image.open('content/fon.png', 'r')
    image = Image.open('content/input.png', 'r')
    width = 200
    height = 265
    resized_img = image.resize((width, height), Image.ANTIALIAS)

    img = Image.new('RGBA', (660, 401), (0, 0, 0, 0))

    img.paste(resized_img, (213, 109))
    img.paste(fon, (0, 0), mask=fon)

    img.save("content/cum.png", format="png")

    upload_url = event.api('photos.getMessagesUploadServer')['upload_url']
    uploaded = requests.post(upload_url, files={'photo': open("content/cum.png", 'rb')}).json()
    a = \
    event.api('photos.saveMessagesPhoto', server=uploaded["server"], photo=uploaded["photo"], hash=uploaded["hash"])[0]
    event.msg_op(2, '', attachment=f'photo{a["owner_id"]}_{a["id"]}', keep_forward_messages=1)
    return "ok"