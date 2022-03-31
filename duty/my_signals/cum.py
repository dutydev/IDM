import requests

from io import BytesIO
from PIL import Image

from duty.utils import path_from_root
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

    width = 200
    height = 265
    out_path = path_from_root('content', 'cum_out.png')

    bg = Image.open(path_from_root('content', 'background.png'), 'r')
    image = Image.open(
        BytesIO(requests.get(url).content)
    ).resize((width, height), Image.ANTIALIAS)

    img = Image.new('RGBA', (660, 401), (0, 0, 0, 0))
    img.paste(image, (213, 109))
    img.paste(bg, (0, 0), mask=bg)
    img.save(out_path, format="png")

    upload_url = event.api('photos.getMessagesUploadServer')['upload_url']
    with open(out_path, 'rb') as out_image:
        uploaded = requests.post(upload_url, files={'photo': out_image}).json()

    att = event.api('photos.saveMessagesPhoto', **uploaded)[0]
    event.edit(
        attachment=f'photo{att["owner_id"]}_{att["id"]}', keep_forward_messages=1
    )
    return "ok"