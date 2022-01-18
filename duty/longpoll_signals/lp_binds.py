from duty.objects import dp, LongpollEvent


@dp.longpoll_event_register('связать', 'отвязать')
def binds_info(event: LongpollEvent):
    event.msg_op(2, 'ℹ️ Для добавления биндов используй префиксы лп модуля ' +
                 '(по умолчанию ".лп", "!лп")')


@dp.longpoll_event_register('бинды', 'связки')
def binds_list(event: LongpollEvent):
    binds = event.db.lp_settings['binds']
    if binds == {}:
        message = ('Пусто. Добавить можно следующим образом:\n' +
                   '{префикс лп модуля} связать {слово}\n{команда}')
    else:
        message = 'Связанные с командами слова:'
        for bind in binds:
            message += f'\n-- "{bind}" -> "{binds[bind]}"'
    event.msg_op(2, message)
