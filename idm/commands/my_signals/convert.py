from ...objects import dp, MySignalEvent
from ...utils import edit_message, new_message, delete_message, sticker_message

@dp.my_signal_event_handle('раск', 'hfcr', 'конв')
def convert(event: MySignalEvent) -> str:
    _eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
    _rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
    _trans_table = dict(zip(_eng_chars, _rus_chars))
    s = ''
    if bool(event.args):
        s = " ".join(event.args)
    if bool(event.payload):
        s = s + '\n' + event.payload
    if event.reply_message != None:
        s = s + '\n' + event.reply_message['text']
    if s == '':
        new_message(event.api, event.chat.peer_id, message='Нет данных 🤦')
    msg = u''.join([_trans_table.get(c, c) for c in s])
    new_message(event.api, event.chat.peer_id, message=msg)
    return "ok"