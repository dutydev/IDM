import requests
from io import StringIO
from os.path import dirname, join
from duty.objects import dp, MySignalEvent


logpath = join(dirname(dirname(dirname(__file__))), f"duty.log")


@dp.my_signal_event_register('лог', skip_receiving=True)
def sticker(event: MySignalEvent) -> str:
    data = StringIO()
    with open(logpath, 'r', encoding='utf-8') as log:
        data.write(log.read())
    data.name = 'log.txt'
    data.seek(0)
    url = event.api('docs.getMessagesUploadServer',
                    type='doc', peer_id=event.chat.peer_id)['upload_url']
    file_data = requests.post(url, files={'file': data}).json()['file']
    doc = event.api('docs.save', file=file_data, title='log.txt')['doc']
    event.msg_op(1, attachment=f"doc{doc['owner_id']}_{doc['id']}")
