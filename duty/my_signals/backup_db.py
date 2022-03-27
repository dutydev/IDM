import requests
from io import StringIO
from os.path import dirname, join
from duty.objects import dp, MySignalEvent


logpath = join(dirname(dirname(dirname(__file__))), f"database.json")

@dp.longpoll_event_register('бекап', 'бд')
@dp.my_signal_event_register('бекап', 'бд', skip_receiving=True)
def sticker(event: MySignalEvent) -> str:
    data = StringIO()
    with open(logpath, 'r', encoding='utf-8') as log:
        data.write(log.read())
    data.name = 'database.json'
    data.seek(0)
    url = event.api('docs.getMessagesUploadServer',
                    type='doc', peer_id=event.chat.peer_id)['upload_url']
    file_data = requests.post(url, files={'file': data}).json()['file']
    doc = event.api('docs.save', file=file_data, title='database.json')['doc']
    event.msg_op(2, "✅ Бекап базы данных отправлен в лс!")
    event.msg_op(1, user_id=event.db.owner_id, attachment=f"doc{doc['owner_id']}_{doc['id']}")