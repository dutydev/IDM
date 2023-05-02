from duty.objects import dp, LongpollEvent, MySignalEvent


@dp.longpoll_event_register('+игнор', '-игнор')
def ignore_info(event: LongpollEvent):
    event.msg_op(2, 'ℹ️ Для добавления в игнор используй префиксы лп модуля ' +
                 '(по умолчанию ".лп", "!лп")')


@dp.longpoll_event_register('игнор', 'игнорлист')
def ignore_list(event: LongpollEvent):
    users = []
    groups = []
    message_u = message_g = ''
    for user in event.db.lp_settings['ignored_users']:
        if int(user) < 0:
            groups.append(user[1:])
        else:
            users.append(user)

    if users:
        message_u = '😶 Игнорируемые пользователи:\n'
        for i, user in enumerate(event.api('users.get',
                                           user_ids=','.join(users)), 1):
            message_u += f"{i}. [id{user['id']}|{user['first_name']} {user['last_name']}]\n"  # noqa

    if groups:
        message_g = '😶 Игнорируемые группы:\n'
        for i, group in enumerate(event.api('groups.getById',
                                            group_ids=','.join(groups)), 1):
            message_g += f"{i}. [public{group['id']}|{group['name']}]\n"

    if not users and not groups:
        message = '💅🏻 Список игнора пуст'
    else:
        message = message_u + '\n' + message_g

    event.api.exe("""API.messages.send({"peer_id":%d,"message":"%s",
                                        "random_id":0,"disable_mentions":1});
        API.messages.delete({"message_ids":%d,"delete_for_all":1});""" % (
            event.chat.peer_id, message.replace('\n', '<br>'), event.msg['id']
        )
    )


@dp.my_signal_event_register('+игнор', '-игнор', 'игнор', 'игнорлист')
def ignore_callback_info(event: MySignalEvent):
    event.edit('ℹ️ В Ирке такое сделать невозможно из-за платформы, '
               'на которой это все дело запускается.\n'
               'Но есть бот гораздо круче, залетай в беседу в группе '
               '@ircaduty, тебе расскажут.')
