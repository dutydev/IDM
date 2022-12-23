import os
import json
import traceback

from typing import Any, Dict, List, Optional
from os.path import join as pjoin

from logger import get_writer

logger = get_writer('База данных')

get_dir = os.path.dirname
core_path = get_dir(get_dir(get_dir(__file__)))

_global_data: Dict[str, Any] = {}


def read(rel_path: str) -> dict:
    'Возвращает словарь из файла с указанным названием'
    try:
        path = pjoin(core_path, rel_path)
        logger.trace(f'Reading "{path}"')
        with open(path, "r", encoding="utf-8") as file:
            return json.loads(file.read())
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


def write(rel_path, data):
    try:
        path = pjoin(core_path, rel_path)
        logger.trace(f'Writing to "{path}"')
        with open(path, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e


class _Responses(dict):
    def __getitem__(self, __k):
        try:
            return super().__getitem__(__k)
        except KeyError:
            return _StandardDefaults.responses.__getitem__(__k)


class __UserDefinedDefaults:
    '''
    запихивай сюда дефолтные значения для своих атрибутов класса БД

    постарайся придумать относительно оригинальное название для своих
    атрибутов, чтобы оно не помешало в будущем кому-то другому добавить
    свои значения (нет, блдяь, не надо называть атрибут "1", опиши адекватно,
    че там, сука, хранится (если совсем туго с мозгами, питон умеет в юникод,
    поэтому можно тупо написать "супер_дупер_данные_жорика"))
    '''


class _StandardDefaults(__UserDefinedDefaults):
    # да, я знаю, что так делать не правильно, но мне похуй, если честно
    owner_id: int = 0
    host: str = ""
    installed: bool = False
    dc_secret: Optional[str] = None
    access_token: str = "Не установлен"
    me_token: str = "Не установлен"
    secret: str = ""
    chats: dict = {}
    trusted_users: List[int] = []
    templates: List[dict] = []
    anims: List[dict] = []
    voices: List[dict] = []

    to_group_saved_group_id: 'int | None' = None

    auth_token: str = ''
    auth_token_date: int = 0

    settings: dict = {
        "silent_deleting": False
    }

    lp_settings: dict = {
        "ignored_users": [],
        "prefixes": [".л", "!л"],
        "binds": {},
        "key": ""
    }

    responses = _Responses({
        "del_self": "&#13;",
        "del_process": "УДАЛЯЮ ЩАЩАЩ ПАДАЖЖЫ",
        "del_success": "✅ *Произошло удаление*",
        "del_err_924": "❗ Не прокатило. Дежурный администратор? 🤔",
        "del_err_vk": "❗ Не прокатило. Ошибка VK:{ошибка}",
        "del_err_not_found": "❗ Не нашел сообщения для удаления 🤷‍♀",
        "del_err_unknown": "❗ Неизвестная ошибка при удалении 👀",
        "chat_subscribe": "РАБОТАЕТ 👍<br>Идентификатор чатика<br>{имя}<br>во вселенной ириса: {ид}",
        "chat_bind": "Чат '{имя}' успешно привязан!",
        "user_ret_ban_expired": "💚 Срок бана пользователя {ссылка} истек",
        "user_ret_process": "💚 Добавляю {ссылка}",
        "user_ret_success": "✅ Пользователь {ссылка} добавлен в беседу",
        "user_ret_err_no_access": "❗ Не удалось добавить {ссылка}.<br>Нет доступа.<br> Возможно, он не в моих друзьях или он уже в беседе",
        "user_ret_err_vk": "❗ Не удалось добавить пользователя {ссылка}.<br>Ошибка ВК.<br>",
        "user_ret_err_unknown": "❗ Не удалось добавить пользователя {ссылка}.<br>Произошла неизвестная ошибка",
        "user_ret_self": "❗ Я уже тут.",
        "to_group_success": "✅ Запись опубликована",
        "to_group_err_forbidden": "❗ Ошибка при публикации. Публикация запрещена. Превышен лимит на число публикаций в сутки, либо на указанное время уже запланирована другая запись, либо для текущего пользователя недоступно размещение записи на этой стене",
        "to_group_err_recs": "❗ Ошибка при публикации. Слишком много получателей",
        "to_group_err_link": "❗ Ошибка при публикации. Запрещено размещать ссылки",
        "to_group_err_vk": "❗ Ошибка при публикации. Ошибка VK:<br>{ошибка}",
        "to_group_err_unknown": "❗ Ошибка при публикации. Неизвестная ошибка",
        "repeat_forbidden_words": [
            "передать",
            "купить",
            "повысить",
            "завещание",
            "модер"
        ],
        "repeat_if_forbidden": "Я это писать не буду.",
        "ping_duty": "{ответ}<br>Ответ за {время}сек.",
        "ping_myself": "{ответ} CB<br>Получено через {время}сек.<br>ВК ответил за {пингвк}сек.<br>Обработано за {обработано}сек.",
        "ping_lp": "{ответ} LP<br>Получено через {время}сек.<br>Обработано за {обработано}сек.",
        "info_duty": "Информация о дежурном:<br>IrCA Duty v{версия}<br>Владелец: {владелец}<br>Чатов: {чаты}<br><br>Информация о чате:<br>Iris ID: {ид}<br>Имя: {имя}",
        "info_myself": "Информация о дежурном:<br>IrCA Duty v{версия}<br>Владелец: {владелец}<br>Чатов: {чаты}<br><br>Информация о чате:<br>Iris ID: {ид}<br>Имя: {имя}",
        "not_in_trusted": "Я тебе не доверяю 😑",
        "trusted_err_no_reply": "❗ Ошибка при выполнении, необходимо пересланное сообщение",
        "trusted_err_in_tr": "⚠ Пользователь уже в доверенных",
        "trusted_err_not_in_tr": "⚠ Пользователь не находился в доверенных",
        "trusted_success_add": "✅ Пользователь {ссылка} в доверенных",
        "trusted_success_rem": "✅ Пользователь {ссылка} удален из доверенных",
        "trusted_list": "Доверенные пользователи:"
    })


class DB(_StandardDefaults):
    'здесь исключительно функционал, значения добавляй в __UserDefinedDefaults'

    def __init__(self):
        _global_data.update(read('database.json'))
        _global_data['responses'] = _Responses(_global_data.get('responses', {}))

    def __getattribute__(self, __name: str) -> Any:
        if __name in _global_data:
            return _global_data[__name]
        obj = object.__getattribute__(self, __name)
        if isinstance(obj, (list, dict, set)):
            obj = obj.copy()
        elif not (isinstance(obj, (str, int, bool, tuple, float)) or obj is None):
            return obj
        _global_data[__name] = obj
        return _global_data[__name]

    def __setattr__(self, __name: str, __value: Any) -> None:
        _global_data[__name] = __value

    def __getitem__(self, __name: str) -> Any:
        return getattr(self, __name)

    def sync(self) -> str:
        'Синхронизирует данные в памяти с файлом'
        write('database.json', _global_data)
        return "ok"


def _update():
    # кто до сих пор не обновился с версии июля 2020 года -
    # - не обновляйтесь нахуй, сидите со своим IDM SC mod
    gen = read('database/general.json')
    usr = read(f'database/{gen["owner_id"]}.json')
    write('database.json', dict(gen, **usr))


try:
    read('database.json')
except (FileNotFoundError, json.JSONDecodeError):
    write('database.json', {})
    try:
        _update()
    except Exception:
        pass

db = DB()  # один пользователь, один поток, один экземпляр, мне стабильно до пизды
