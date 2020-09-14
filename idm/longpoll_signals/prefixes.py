from idm.objects import dp, LongpollEvent


@dp.longpoll_event_register('+префикс', '-префикс')
def binds_info(event: LongpollEvent):
    event.msg_op(2, 'ℹ️ Для добавления биндов используй префиксы лп модуля ' +
                 '(по умолчанию ".лп", "!лп")')


@dp.longpoll_event_register('бинды', 'связки')
def binds_list(event: LongpollEvent):
    prefixes = event.db.lp_settings['prefixes']
    if not prefixes:
        message = ('Я не знаю как ты этого достиг, но у тебя нет ни одного ' +
                   'LP префикса. На всякий случай добавил префикс "!л", ' +
                   'можешь пользоваться им')
        event.db.lp_settings['prefixes'].append('!л')
        event.db.save()
    else:
        message = 'Префиксы LP сигналов:'
        for prefix in prefixes:
            message += f'\n-- "{prefix}"'
    event.msg_op(2, message)
