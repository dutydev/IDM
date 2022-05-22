from io import BytesIO
import requests
from duty.objects import dp, MySignalEvent


# Прошу прощения за говнокод. Лень было функцию для загрузки делать :)
@dp.longpoll_event_register('неко')
@dp.my_signal_event_register('неко')
def neko(event: MySignalEvent) -> str:
    event.msg_op(2, "⏱️Секунду...")
    img_url = requests.get("https://api.loli-art.ru/arts?count=1").json()["arts"][0]
    image = BytesIO(requests.get(url=img_url).content)
    image.name = 'neko.jpg'
    upload_url = event.api('photos.getMessagesUploadServer')['upload_url']
    data = requests.post(upload_url, files={'photo': image}).json()
    del (image)
    saved = event.api('photos.saveMessagesPhoto', photo=data['photo'],
                      hash=data['hash'], server=data['server'])[0]
    event.msg_op(2, "Держи свою Неко :)", attachment=f"photo{saved['owner_id']}_{saved['id']}_{saved['access_key']}")


@dp.longpoll_event_register('лоли')
@dp.my_signal_event_register('лоли')
def loli(event: MySignalEvent) -> str:
    event.msg_op(2, "⏱️Секунду...")
    img_url = requests.get("https://api.loli-art.ru/arts?count=1").json()["arts"][0]
    image = BytesIO(requests.get(url=img_url).content)
    image.name = 'neko.jpg'
    upload_url = event.api('photos.getMessagesUploadServer')['upload_url']
    data = requests.post(upload_url, files={'photo': image}).json()
    del (image)
    saved = event.api('photos.saveMessagesPhoto', photo=data['photo'],
                      hash=data['hash'], server=data['server'])[0]
    event.msg_op(2, "Держи свою Лоли :)", attachment=f"photo{saved['owner_id']}_{saved['id']}_{saved['access_key']}")


@dp.longpoll_event_register('хентай')
@dp.my_signal_event_register('хентай')
def neko_hentai(event: MySignalEvent) -> str:
    event.msg_op(2, "⏱️Секунду...")
    img_urls = requests.get("https://api.waifu.pics/nsfw/neko").json()['url']
    image = BytesIO(requests.get(url=img_urls).content)
    image.name = 'neko.jpg'
    upload_url = event.api('photos.getMessagesUploadServer')['upload_url']
    data = requests.post(upload_url, files={'photo': image}).json()
    del (image)
    saved = event.api('photos.saveMessagesPhoto', photo=data['photo'],
                      hash=data['hash'], server=data['server'])[0]
    event.msg_op(2, "Держи свой хентай :)", attachment=f"photo{saved['owner_id']}_{saved['id']}_{saved['access_key']}")
