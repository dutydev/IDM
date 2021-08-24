from idm.objects import dp, MySignalEvent, db_gen
from idm.utils import find_mention_by_event, get_plural, cmid_key
from typing import Union
import requests

session = None

DC = 'https://IrcaDC.pythonanywhere.com'

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


@dp.longpoll_event_register('цод')
@dp.my_signal_event_register('цод')
def dc(event: MySignalEvent):
    resp = requests.post(DC, json={
        'method': 'info',
        'user_id': str(event.db.duty_id),
        'session': session
    }, timeout=5)
    if resp.status_code != 200:
        if resp.status_code == 403:
            return "ok"
        event.msg_op(1, '❗ Проблемы с центром обработки данных\n' +
                     'Напиши [id332619272|этому челику], если он еще живой',
                     disable_mentions=1)
        return "ok"
    users = resp.json()['users']
    event.msg_op(2, f'Зарегистрировано {users} пользовател{get_plural(users, "ь", "я", "ей")}')  # noqa
    return "ok"


@dp.longpoll_event_register('унапиши', 'у')
@dp.my_signal_event_register('унапиши', 'у')
def remote_control(event: MySignalEvent) -> Union[str, dict]:
    if db_gen.dc_auth is False:
        event.msg_op(2, '❗ Для использования этой команды необходимо ' +
                     'разрешить авторизацию в ЦОД по токену (на сайте)')
        return "ok"

    uid = find_mention_by_event(event)
    if uid is None:
        event.msg_op(2, '❗ Необходимо указать пользователя')
        return "ok"

    resp = requests.post(DC, json={
        'method': 'remote_control',
        'remote_user': str(uid),
        'user_id': str(event.db.duty_id),
        'session': session,
        'data': {
            'chat': event.chat.iris_id,
            'local_id': event.msg[cmid_key]
        }
    }, timeout=5)
    if resp.status_code != 200:
        event.msg_op(1, '❗ Проблемы с центром обработки данных\n' +
                     'Напиши [id332619272|этому челику], если он еще живой',
                     disable_mentions=1)
        return "ok"

    resp = resp.json()

    if 'error' in resp:
        code = resp['error']
        if code == 5:
            msg = f"❗ Ошибка VK #{resp['code']}: {resp['msg']}"
        else:
            msg = errors.get(code, '❗ Неизвестный код ошибки')
        event.msg_op(2, msg)
        return "ok"

    event.msg_op(3)
    return "ok"
