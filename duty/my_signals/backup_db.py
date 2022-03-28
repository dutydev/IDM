from io import StringIO
from time import sleep
from os.path import join

import requests

from duty.objects import dp, MySignalEvent, database


path = join(database.core_path, f"database.json")


@dp.longpoll_event_register('бекап', 'бэкап', 'бд')
@dp.my_signal_event_register('бекап', 'бэкап', 'бд', skip_receiving=True)
def sticker(event: MySignalEvent) -> str:
    data = StringIO()
    data.name = 'database.json'
    with open(path, 'r', encoding='utf-8') as file:
        data.write(file.read())
    data.seek(0)
    url = event.api('docs.getMessagesUploadServer',
                    type='doc', peer_id=event.chat.peer_id)['upload_url']
    file_data = requests.post(url, files={'file': data}).json()['file']
    doc = event.api('docs.save', file=file_data, title='database.json')['doc']
    event.send(
        user_id=event.db.owner_id,
        attachment=f"doc{doc['owner_id']}_{doc['id']}"
    )
    sleep(0.5)
    event.edit("✅ Копия базы данных отправлена в избранное.")
