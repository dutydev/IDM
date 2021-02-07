from ...objects import dp, MySignalEvent
from ...utils import edit_message


@dp.my_signal_event_handle('+дов')
def add_trusted_user(event: MySignalEvent) -> str:
    if event.reply_message is None:
        edit_message(event.api, event.chat.peer_id, event.msg['id'],
                     message="❗ Ошибка при выполнении, необходимо пересланное сообщение")
        return "ok"

    tr_id = event.reply_message['from_id']
    if tr_id in event.db.trusted_users:
        edit_message(event.api, event.chat.peer_id, event.msg['id'],
                     message=f"⚠ Пользователь уже в доверенных.")
        return "ok"
    tr_user = event.api('users.get', user_ids=tr_id)[0]
    event.db.trusted_users.append(tr_id)
    event.db.save()
    edit_message(event.api, event.chat.peer_id, event.msg['id'],
                 message=f"✅ Пользователь "
                         f"[id{tr_user['id']}|{tr_user['first_name']} {tr_user['last_name']}] в доверенных.")
    return "ok"


@dp.my_signal_event_handle('-дов')
def remove_trusted_user(event: MySignalEvent) -> str:
    if event.reply_message is None:
        edit_message(event.api, event.chat.peer_id, event.msg['id'],
                     message="❗ Ошибка при выполнении, необходимо пересланное сообщение")
        return "ok"

    tr_id = event.reply_message['from_id']
    if tr_id not in event.db.trusted_users:
        edit_message(event.api, event.chat.peer_id, event.msg['id'],
                     message=f"⚠ Пользователь не находился в доверенных.")
        return "ok"

    tr_user = event.api('users.get', user_ids=tr_id)[0]
    event.db.trusted_users.remove(tr_id)
    event.db.save()
    edit_message(event.api, event.chat.peer_id, event.msg['id'],
                 message=f"✅ Пользователь "
                         f"[id{tr_user['id']}|{tr_user['first_name']} {tr_user['last_name']}] удален из доверенных.")
    return "ok"


@dp.my_signal_event_handle('доверенные', "довы")
def trusted_users(event: MySignalEvent) -> str:
    users = event.api('users.get', user_ids=",".join([str(i) for i in event.db.trusted_users]))

    message = "Доверенные пользователи:"
    itr = 0
    for user in users:
        itr += 1
        message += f"\n{itr}. [id{user['id']}|{user['first_name']} {user['last_name']}]"

    edit_message(event.api, event.chat.peer_id, event.msg['id'], message=message)

    return "ok"
