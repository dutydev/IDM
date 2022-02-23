import time

from duty.objects import dp, MySignalEvent, db
from duty.utils import find_mention_by_event, get_plural, cmid_key
from typing import Union
import requests
from microvk import VkApi, VkApiResponseException
from flask import  request

session = None

DC = 'https://api.lisi4ka.ru/'
group_dc = -201667822

errors = {
    4: ('❗ На удаленном сервере отсутствует данный чат\n' +
        'Необходимо связать чат (на том аккаунте, не на этом)'),
    3: '❗ Неверная сессия. Перезапусти дежурного',
    2: '❗ Удаленный дежурный тебе не доверяет',
    1: '❗ Неизвестная ошибка на удаленном сервере',
    0: '❗ Пользователь не зарегистрирован\nВозможно у него старая версия дежурного'  # noqa
}


def set_session(ses: str) -> str:
    global session
    session = ses
    return ses


@dp.longpoll_event_register('+цод')
@dp.my_signal_event_register('+цод')
def reg_dc(event: MySignalEvent):
    protocol = 'https' if 'pythonanywhere' in request.host else 'http'
    VkApi(db.access_token).msg_op(1, group_dc, f'+cod {db.secret} {protocol}://{request.host}/')
    time.sleep(0.5)
    event.msg_op(2, f'Запрос отправлен. Иди проверяй.')
    return "ok"


@dp.longpoll_event_register('чек')
@dp.my_signal_event_register('чек')
def check(event: MySignalEvent):
    uid = find_mention_by_event(event)
    resp = requests.get(DC + f'reg/{uid}', timeout=10)
    if resp.status_code != 200:
        event.msg_op(1, '❗ Проблемы с центром обработки данных\n' +
        'Напиши [id230192963|этому челику], если он еще живой',
        disable_mentions = 1)
        return "ok"

    r = resp.json()
    if r['status'] == 'error':
        msg = r['error']
        event.msg_op(2, msg)
        return "ok"
    else:
        msg = f'[id{uid}|Пользователь] {"" if r["is_registered"] == 1 else "не"} зарегестрирован.'
        event.msg_op(2, msg)
        return "ok"


@dp.longpoll_event_register('цод')
@dp.my_signal_event_register('цод')
def dc(event: MySignalEvent):
    print('cod')
    resp = requests.get(DC + 'stat', timeout=10)
    if resp.status_code != 200:
        event.msg_op(1, '❗ Проблемы с центром обработки данных\n' +
                     'Напиши [id230192963|этому челику], если он еще живой',
                     disable_mentions=1)
        return "ok"
    users = resp.json()['count']
    event.msg_op(2, f'Зарегистрировано {users} пользовател{get_plural(users, "ь", "я", "ей")}')
    return 'ok'


@dp.longpoll_event_register('унапиши', 'у')
@dp.my_signal_event_register('унапиши', 'у')
def remote_control(event: MySignalEvent) -> Union[str, dict]:
    uid = find_mention_by_event(event)
    if uid is None:
        event.msg_op(2, '❗ Необходимо указать пользователя')
        return "ok"

    resp = requests.post(DC + 'repeat', json={
        'user_id': uid,
        'owner_id': event.db.owner_id,
        'chat': event.chat.iris_id,
        'local_id': event.msg[cmid_key],
        'secret': db.secret
    }, timeout=10)
    if resp.status_code != 200:
        event.msg_op(1, '❗ Проблемы с центром обработки данных\n' +
                     'Напиши [id230192963|этому челику], если он еще живой',
                     disable_mentions=1)
        return "ok"

    r = resp.json()

    if r['status'] == 'error':
        msg = r['error']
        event.msg_op(2, msg)
        return "ok"

    event.msg_op(3)
    return "ok"
