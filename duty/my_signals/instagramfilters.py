from duty.objects import MySignalEvent, dp
import requests, os


@dp.longpoll_event_register('инст')
@dp.my_signal_event_register('инст')
def initial(event: MySignalEvent) -> str:
    try:
        from instafilter import Instafilter
    except ImportError:
        event.msg_op(2, 'Скачиваю зависимость...')
        os.system('python3.8 -m pip install git+https://github.com/Obnovlator3000/instafilter.git')
        __import__('uwsgi').reload()
        event.msg_op(2, 'Перезагружаюсь... На всякий случай, после этого пропиши ".с инст"')
    try:
        import cv2
        event.msg_op(2, 'Все готово!')
    except ImportError:
        event.msg_op(2, 'Скачиваю зависимость...')
        os.system('python3.8 -m pip install opencv-python')
        __import__('uwsgi').reload()
        event.msg_op(2, 'Перезагружаюсь...')
    return "ok"


@dp.longpoll_event_register('фильтры')
@dp.my_signal_event_register('фильтры')
def filternames(event: MySignalEvent) -> str:
    event.msg_op(2, "Список фильтров и их отличия: https://vk.com/@ircaduty-insta-filtry")


@dp.longpoll_event_register('фильтр')
@dp.my_signal_event_register('фильтр')
def insta(event: MySignalEvent) -> str:
    try:
        from instafilter import Instafilter
        import cv2
    except ImportError:
        event.msg_op(1, 'Сначала нужно доустановить одну зависимость, щас сделаю...')
        event.msg_op(1, f'{event.msg["text"].split()[0]} инст')
        return "ok"
    if not (event.attachments or event.reply_message):
            event.msg_op(2, "❗ Нет данных")
            return "ok"

    if event.reply_message:
        event.attachments = event.reply_message['attachments']
        print(event.attachments)
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
    out = open(os.path.join(os.getcwd(), 'input.png'), "wb")
    out.write(r.content)
    out.close()

    filtername = event.msg['text'].split()[-1]
    filters = ['1977', 'Aden', 'Amaro', 'Ashby', 'Brannan', 'Brooklyn', 'Charmes', 'Clarendon', 'Crema', 'Dogpatch', 'Earlybird', 'Gingham', 'Ginza', 'Hefe', 'Helena', 'Hudson', 'Inkwell', 'Juno', 'Kelvin', 'Lark', 'Lo-Fi', 'Ludwig', 'Mayfair', 'Melvin', 'Moon', 'Nashville', 'Perpetua', 'Reyes', 'Rise', 'Sierra', 'Skyline', 'Slumber', 'Stinson', 'Sutro', 'Toaster', 'Valencia', 'Vesper', 'Walden', 'Willow', 'X-ProII']
    if filtername == 'фильтр' or filtername not in filters:
        event.msg_op(2, f'Доступные фильтры: {", ".join(filters)}')
        return "ok"
    model = Instafilter(filtername)
    new_image = model(os.path.join(os.getcwd(), 'input.png'))
    cv2.imwrite("output.png", new_image)
    upload_url = event.api('photos.getMessagesUploadServer')['upload_url']
    uploaded = requests.post(upload_url, files={'photo': open("output.png", 'rb')}).json()
    a = event.api('photos.saveMessagesPhoto', server=uploaded["server"], photo=uploaded["photo"], hash=uploaded["hash"])[0]
    event.msg_op(2, '', attachment=f'photo{a["owner_id"]}_{a["id"]}')
    
    os.remove('input.png')
    os.remove("output.png")
    return "ok"
