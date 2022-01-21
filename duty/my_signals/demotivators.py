from duty.objects import MySignalEvent, dp
import requests, os
from simpledemotivators import Demotivator


@dp.my_signal_event_register('дем')
def dem(event: MySignalEvent) -> str:
    if not (event.attachments or event.reply_message):
        event.msg_op(2, "❗ Нет данных")
        return "ok"

    if event.reply_message:
        event.attachments = event.reply_message['attachments']
        print(event.attachments)
        if event.attachments:
            if event.attachments[0]['type'] != 'photo':
                event.msg_op(2, 'Как я тебе не из картинки сделаю демотиватор?')
                return "ok"
            url = event.attachments[0]['photo']['sizes'][-1]['url']
    else:
        if event.msg['attachments'][0]['type'] != 'photo':
            event.msg_op(2, 'Как я тебе не из картинки сделаю демотиватор?')
            return "ok"
        url = event.msg['attachments'][0]['photo']['sizes'][-1]['url']
    r = requests.get(url)
    out = open('input.png', "wb")
    out.write(r.content)
    out.close()
    args = event.msg['text'].split('\n')
    args.append('')
    try:
        dem = Demotivator(args[1], args[2])
        dem.create('input.png')
    except:
        dem = Demotivator('А чё писать то?', '')
        dem.create('input.png')
    upload_url = event.api('photos.getMessagesUploadServer')['upload_url']
    uploaded = requests.post(upload_url, files={'photo': open("output.png", 'rb')}).json()
    a = event.api('photos.saveMessagesPhoto', server=uploaded["server"], photo=uploaded["photo"], hash=uploaded["hash"])[0]
    event.msg_op(2, '', attachment=f'photo{a["owner_id"]}_{a["id"]}')
    os.remove('input.png')
    os.remove("output.png")
    return "ok"





