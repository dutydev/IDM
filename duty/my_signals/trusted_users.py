from duty.objects import dp, MySignalEvent
from duty.utils import ment_user, format_response
from duty.utils import find_mention_by_event


def tr_user_op(event, error, typ):
    tr_id = find_mention_by_event(event)

    if not tr_id:
        event.msg_op(2, event.responses['trusted_err_no_reply'])
        return "ok"

    def tr_err():
        event.msg_op(2, event.responses[f'trusted_err_{error}'])
        return "ok"

    tr_id = event.reply_message['from_id'] if event.reply_message else tr_id
    if typ == 'add':
        if tr_id in event.db.trusted_users: return tr_err()
    else:
        if tr_id not in event.db.trusted_users: return tr_err()

    tr_user = event.api('users.get', user_ids=tr_id)[0]

    if typ == 'add':
        event.db.trusted_users.append(tr_id)
    else:
        event.db.trusted_users.remove(tr_id)

    # TODO: избавиться от этих msg_op
    event.msg_op(2, format_response(event.responses[f'trusted_success_{typ}'], 
                 ссылка=ment_user(tr_user)))
    return "ok"


@dp.longpoll_event_register('+дов', "доверять")
@dp.my_signal_event_register('+дов', "доверять")
def add_trusted_user(event: MySignalEvent) -> str:
    return tr_user_op(event, 'in_tr', 'add')


@dp.longpoll_event_register('-дов', 'перестать')
@dp.my_signal_event_register('-дов', 'перестать')
def remove_trusted_user(event: MySignalEvent) -> str:
    return tr_user_op(event, 'not_in_tr', 'rem')


@dp.longpoll_event_register('доверенные', 'довы')
@dp.my_signal_event_register('доверенные', 'довы')
def trusted_users(event: MySignalEvent) -> str:
    users = event.api('users.get', user_ids=",".join([str(i) for i in event.db.trusted_users]))

    message = event.responses['trusted_list']
    itr = 0
    for user in users:
        itr += 1
        message += f"\n{itr}. [id{user['id']}|{user['first_name']} {user['last_name']}]"
    
    event.msg_op(2, message)

    return "ok"
