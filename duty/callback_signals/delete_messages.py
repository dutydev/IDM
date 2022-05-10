from duty.objects import dp, Event
from duty.utils import ment_user, cmid_key, format_response
from duty.api_utils import get_msgs
from datetime import datetime
import time


def msg_delete(event, msg_id, msg_ids=[]):
    if getattr(event, 'msg'):
        if event.msg['from_id'] == event.db.owner_id and not msg_ids:
            event.obj['local_ids'].append(event.msg[cmid_key])

    def del_edit(key, err=''):
        if not event.obj['silent']:
            event.edit_msg(msg_id, format_response(event.responses[key], ошибка=err))
            time.sleep(3)
            event.api.msg_op(3, msg_id=msg_id)

    if msg_ids:
        code = """return API.messages.delete({delete_for_all: 1,
        message_ids:%s});""" % (msg_ids)
    else:
        code = """return API.messages.delete({delete_for_all: 1, message_ids:
        API.messages.getByConversationMessageId({peer_id:"%s",
        conversation_message_ids:%s}).items@.id});""" % (
            event.chat.peer_id, event.obj['local_ids'])

    while True:
        ret = event.api.exe(code)
        if "error" not in ret:
            del_edit('del_success')
            break
        elif ret['error']['error_code'] == 6:
            time.sleep(0.4)
        else:
            e = ret['error']
            if e['error_code'] == 924: del_edit('del_err_924')
            else: del_edit('del_err_vk', e['error_msg'])
            break

    return "ok"


def del_info(event):
    if not event.obj['silent']:
        return event.api.msg_op(1, event.chat.peer_id, event.responses['del_process'])


@dp.event_register('deleteMessages')
def delete_messages(event: Event) -> str:
    return msg_delete(event, del_info(event))


@dp.event_register('deleteMessagesFromUser')
def delete_messages_from_user(event: Event) -> str:
    event.obj['silent'] = False

    amount = event.obj.get("amount")

    msg_ids = []
    ct = datetime.now().timestamp()

    for msg in get_msgs(event.chat.peer_id, event.api):
        if ct - msg['date'] >= 86400: break
        if msg['from_id'] in event.obj['member_ids'] and not msg.get('action'):
            msg_ids.append(msg['id'])

    if amount:
        if amount < len(msg_ids):
            msg_ids = msg_ids[:len(msg_ids) - (len(msg_ids) - amount)]

    if not msg_ids:
        event.api.msg_op(1, event.chat.peer_id, event.responses['del_err_not_found'])
        return "ok"

    return msg_delete(event, del_info(event), msg_ids)


@dp.event_register('messages.deleteByType')
def delete_by_type(event: Event) -> str:
    event.obj['silent'] = False

    typ = event.obj['type']
    if typ == 'stickers': typ = 'sticker'
    elif typ == 'voice': typ = 'audio_message'
    elif typ == 'gif': typ = 'doc'
    elif typ == 'article': typ = 'link'

    msg_ids = []
    ct = (event.obj['time'] + 86400 if event.obj.get('time')
          else datetime.now().timestamp())

    amount = event.obj.get('amount', 1000)

    null_admins = False

    if not event.obj['admin_ids']:
        null_admins = True
        event.obj['admin_ids'] = []
    else:
        if type(event.obj['admin_ids']) == str:
            event.obj['admin_ids'] = event.obj['admin_ids'].split(',')
        if type(event.obj['admin_ids'][0]) == str:
            event.obj['admin_ids'] = [int(i) for i in event.obj['admin_ids']]

    users = {}

    def append(msg):
        msg_ids.append(msg['id'])
        users.update({msg['from_id']: users.get(msg['from_id'], 0) + 1})

    if typ in {'any', 'period'}:
        for msg in get_msgs(event.chat.peer_id, event.api):
            if ct - msg['date'] > 86400 or len(msg_ids) == amount:
                break
            if msg['from_id'] in event.obj['admin_ids']:
                continue
            append(msg)
    else:
        for msg in get_msgs(event.chat.peer_id, event.api):
            atts = msg.get('attachments')
            if ct - msg['date'] > 86400 or len(msg_ids) == amount:
                break
            if msg['from_id'] in event.obj['admin_ids']:
                continue
            if typ == 'forwarded' and msg['fwd_messages']:
                append(msg)
            elif atts:
                for att in atts:
                    if att['type'] == typ:
                        append(msg)
                    elif typ == 'doc' and att.get('doc'):
                        if att['doc'].get('ext') == 'gif':
                            append(msg)
                    elif typ == 'link' and att.get('link'):
                        if att['link'].get('description') == 'Article':
                            append(msg)

    if not msg_ids:
        event.api.msg_op(1, event.chat.peer_id, event.responses['del_err_not_found'])
        return "ok"

    event.obj['silent'] = True
    event.api.raise_excepts = False

    msg_delete(event, del_info(event), msg_ids)

    if null_admins:
        event.api.msg_op(1, event.chat.peer_id, 'Ирис не прислал список администраторов.' +
                         'Попробуй обновить чат (команда "обновить чат")')
        return "ok"

    message = 'Удалены сообщения следующих пользователей:\n'

    for user in event.api('users.get', user_ids=','.join([str(i) for i in users.keys()])):
        message += f'{ment_user(user)} ({users.get(user["id"])})\n'

    event.api.msg_op(1, event.chat.peer_id, message, disable_mentions=1)
    return "ok"
