from ..objects import dp, Event
from ..utils import new_message, edit_message, delete_message
from ..lpcommands.utils import exe, get_msgs
from datetime import datetime
import time

def msg_delete(event, msg_id, msg_ids = []):
    if getattr(event, 'msg'):
        if event.msg['from_id'] == event.db.duty_id and not msg_ids:
            event.obj['local_ids'].append(event.msg['conversation_message_id'])

    def del_edit(key, err = ''):
        if not event.obj['silent']:
            edit_message(event.api, event.chat.peer_id, msg_id,
            message = event.responses[key].format(ошибка = err))
            time.sleep(3)
            delete_message(event.api, event.chat.peer_id, msg_id)

    if msg_ids:
        code = """return API.messages.delete({delete_for_all: 1,
        message_ids:%s});""" % (msg_ids)
    else:
        code = """return API.messages.delete({delete_for_all: 1, message_ids:
        API.messages.getByConversationMessageId({peer_id:"%s",
        conversation_message_ids:%s}).items@.id});""" % (
        event.chat.peer_id, event.obj['local_ids'])

    while True:
        ret = exe(code)
        if not "error" in ret:
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
        return new_message(event.api, event.chat.peer_id, message=event.responses['del_process'])


@dp.event_handle('deleteMessages')
def delete_messages(event: Event) -> str:
    return msg_delete(event, del_info(event))


@dp.event_handle('deleteMessagesFromUser')
def delete_messages_from_user(event: Event) -> str:
    event.obj['silent'] = False

    amount = event.obj.get("amount")

    msg_ids = []
    ct = datetime.now().timestamp()

    for msg in get_msgs(event.chat.peer_id):
        if ct - msg['date'] >= 86400: break
        if msg['from_id'] in event.obj['member_ids'] and not msg.get('action'):
            msg_ids.append(msg['id'])

    if amount:
        if amount < len(msg_ids):
            msg_ids = msg_ids[:len(msg_ids) - (len(msg_ids) - amount)]

    if not msg_ids:
        edit_message(event.api, event.chat.peer_id, msg_id,
        message=event.responses['del_err_not_found'])
        return "ok"

    return msg_delete(event, del_info(event), msg_ids)
    

@dp.event_handle('messages.deleteByType')
def delete_by_type(event: Event) -> str:
    event.obj['silent'] = False

    typ = event.obj['type']
    if typ == 'stickers': typ = 'sticker'
    elif typ == 'voice': typ = 'audio_message'
    elif typ == 'gif': typ = 'doc'
    elif typ == 'article': typ = 'link'

    msg_ids = []
    ct = datetime.now().timestamp()

    for msg in get_msgs(event.chat.peer_id):
        atts = msg.get('attachments')
        if ct - msg['date'] > 86400: break
        if typ == 'forwarded' and msg['fwd_messages']:
            msg_ids.append(msg['id'])
        elif atts:
            for att in atts:
                if att['type'] == typ:
                    msg_ids.append(msg['id'])
                elif typ == 'doc' and att.get('doc'):
                    if att['doc'].get('ext') == 'gif':
                        msg_ids.append(msg['id'])
                elif typ == 'link' and att.get('link'):
                    if att['link'].get('description') == 'Article':
                        msg_ids.append(msg['id'])

    if not msg_ids:
        edit_message(event.api, event.chat.peer_id, msg_id,
        message=event.responses['del_err_not_found'])
        return "ok"

    return msg_delete(event, del_info(event), msg_ids)

