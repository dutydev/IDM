import time

from duty.objects import dp, MySignalEvent, db
from duty.utils import find_mention_by_event, get_plural, cmid_key
from typing import Union
import requests
from microvk import VkApi
from flask import  request


DC_HOST = 'https://api.lisi4ka.ru/'
DC_GROUP_ID = -195759899

errors = {
    0: (
        '❗ Пользователь не зарегистрирован\n'
        'Возможно у него старая версия дежурного'
    ),
    1: '❗ Неизвестная ошибка на удаленном сервере',
    2: '❗ Удаленный дежурный тебе не доверяет',
    3: '❗ Неверная сессия. Перезапусти дежурного',
    4: (
        '❗ На удаленном сервере отсутствует данный чат\n'
        'Необходимо связать чат (на том аккаунте, не на этом)'
    ),
}


class RequestError(Exception):
    pass


def make_dc_request(event: MySignalEvent, path: str, **data):
    data.update({'owner_id': event.db.owner_id, 'secret': db.dc_secret})
    resp = requests.get(DC_HOST + path, timeout=10, json=data)
    if resp.status_code != 200:
        event.send(
            '❗ Проблемы с центром обработки данных\n'
            'Напиши [id230192963|этому челику], если он еще живой',
            disable_mentions=1
        )
        raise RequestError
    decoded_response = resp.json()
    if decoded_response.get('status') == 'error':
        event.edit(str(decoded_response['error']))
        raise RequestError
    return decoded_response


@dp.longpoll_event_register('+цод')
@dp.my_signal_event_register('+цод')
def reg_dc(event: MySignalEvent):
    db.dc_auth = True
    protocol = 'https' if 'pythonanywhere' in request.host else 'http'
    VkApi(db.access_token).msg_op(
        1, DC_GROUP_ID, f'+cod {db.secret} {protocol}://{request.host}/'
    )
    time.sleep(0.5)  # антикапча от лиса
    event.msg_op(2, f'🆗 Запрос отправлен. Иди проверяй.')
    return "ok"


@dp.longpoll_event_register('цод')
@dp.my_signal_event_register('цод')
def dc(event: MySignalEvent):
    try:
        users = make_dc_request(event, 'stat')['count']
    except RequestError:
        pass
    else:
        event.msg_op(2,
            f'👥 Зарегистрировано {users} пользовател' +
            get_plural(users, "ь", "я", "ей")
        )
    return 'ok'


@dp.longpoll_event_register('чц')
@dp.my_signal_event_register('чц')
def chdc(event: MySignalEvent):
    try:
        make_dc_request(event, 'check')
    except RequestError:
        pass
    else:
        event.msg_op(2, 'Всё хорошо')
    return "ok"


@dp.longpoll_event_register('чек')
@dp.my_signal_event_register('чек')
def check(event: MySignalEvent):
    uid = find_mention_by_event(event)
    if uid is None:
        event.edit(f'❗ Не указан пользователь.')
        return "ok"

    try:
        reg = make_dc_request(event, f'reg/{uid}')['is_registered']
    except RequestError:
        return "ok"

    if reg:
        event.edit(f'🥑 [id{uid}|Пользователь] зарегистрирован.')
    else:
        event.edit(f'🗿 [id{uid}|Пользователь] не зарегистрирован.')
    return "ok"


@dp.longpoll_event_register('унапиши', 'у')
@dp.my_signal_event_register('унапиши', 'у')
def remote_control(event: MySignalEvent) -> Union[str, dict]:
    uid = find_mention_by_event(event)
    if uid is None:
        event.msg_op(2, '❗ Необходимо указать пользователя')
        return "ok"

    try:
        make_dc_request(
            event,
            'repeat',
            user_id=uid,
            chat=event.chat.iris_id,
            local_id=event.msg[cmid_key]
        )
    except RequestError:
        pass
    else:
        event.msg_op(3)
    return "ok"
