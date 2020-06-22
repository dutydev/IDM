from . import dlp
from .utils import parseByID, find_mention_by_message, ExcReload, msg_op
from time import sleep


@dlp.register_startswith('+игнор')
def ignore_add(nd):
    user_id = find_mention_by_message(parseByID(nd[1]))
    if not user_id:
        msg = '❗ Необходимо пересланное сообщение или упоминание'
    else:
        if str(user_id) in nd.db.settings['ignore_list']:
            msg = '👀 Уже...'
        else:
            nd.db.settings['ignore_list'].append(str(user_id))
            msg = '🚷 Добавлено'
    msg_op(2, nd[3], msg, nd[1])
    sleep(1)
    msg_op(3, nd[3], msg_id = nd[1])
    if msg == '🚷 Добавлено':
        nd.db.save()
        raise ExcReload(nd.db.gen.group_id)


@dlp.register_startswith('-игнор')
def ignore_add(nd):
    user_id = find_mention_by_message(parseByID(nd[1]))
    if not user_id:
        msg = '❗ Необходимо пересланное сообщение или упоминание'
    else:
        if str(user_id) in nd.db.settings['ignore_list']:
            nd.db.settings['ignore_list'].remove(str(user_id))
            msg = '💅🏻 Удалено'
        else:
            msg = '🤷‍♀ Не в списке'
    msg_op(2, nd[3], msg, nd[1])
    sleep(1)
    msg_op(3, nd[3], msg_id = nd[1])
    if msg == '💅🏻 Удалено':
        nd.db.save()
        raise ExcReload(nd.db.gen.group_id)