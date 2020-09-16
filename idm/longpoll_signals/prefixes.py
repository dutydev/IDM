from idm.objects import dp, LongpollEvent, MySignalEvent


@dp.longpoll_event_register('+префикс', '-префикс')
def binds_info(event: LongpollEvent):
    event.msg_op(2, 'ℹ️ Для добавления биндов используй префиксы лп модуля ' +
                 '(по умолчанию ".лп", "!лп")')


@dp.longpoll_event_register('префиксы')
def binds_list(event: LongpollEvent):
    prefixes = event.db.lp_settings['prefixes']
    if not prefixes:
        message = ('Я не знаю как ты этого достиг, но у тебя нет ни одного ' +
                   'LP префикса. На всякий случай добавил префикс "!л", ' +
                   'можешь пользоваться им (возможно понадобится ' +
                   'перезапуск LP модуля)')
        event.db.lp_settings['prefixes'].append('!л')
        event.db.save()
    else:
        message = 'Префиксы LP сигналов:'
        for prefix in prefixes:
            message += f'\n-- "{prefix}"'
    event.msg_op(2, message)


@dp.my_signal_event_register('+префикс', '-префикс')
def prefixes_callback_info(event: MySignalEvent):
    event.msg_op(2, 'ℹ️ Менять префиксы можно только через LP модуль\n' +
                 'https://github.com/Elchinchel/ICAD-Longpoll')
