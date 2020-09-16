# тут (да и не только тут) есть много странных костылей,
# большинство из них предназначено для обратной совместимости (ну или мне просто лень было их убирать)
import json
import os
from typing import List

from wtflog import warden

logger = warden.get_boy('База данных')

get_dir = os.path.dirname # p = это os.path, если че)
path = os.path.join(get_dir(get_dir(get_dir(__file__))), 'database')


db_gen: "DB_general"


def read(name: str) -> dict:
    'Возвращает словарь из файла с указанным названием'
    logger.debug(f'Открываю файл "{name}"')
    with open(os.path.join(path, f'{name}.json'), "r", encoding="utf-8") as file:
        return json.loads(file.read())


gen_raw = {
    "owner_id": 0,
    "vk_app_id": 0,
    "vk_app_secret": "",
    "host": "",
    "installed": False,
    "dc_auth": False
}


def create_general():
    try:
        with open(os.path.join(path, 'general.json'), "w", encoding="utf-8") as file:
            file.write(json.dumps(gen_raw, ensure_ascii=False, indent=4))
    except FileNotFoundError:
        os.mkdir(path)
        create_general()


try:
    read('general')
except FileNotFoundError:
    create_general()


class ExcDB(Exception):
    code: int
    text: str

    def __init__(self, code):
        self.code = int(code)
        if self.code == 0:
            self.text = "В админ панель можно зайти только с аккаунта дежурного 💅🏻"
        elif self.code == 1:
            self.text = 'Ошибка БД: Указанный ID уже добавлен в базу'
        else:
            self.text = code


class DB_defaults:

    settings: dict = {
        "silent_deleting": False
    }

    lp_settings: dict = {
        "ignored_users": [],
        "prefixes": [".л", "!л"],
        "binds": {},
        "key": ""
    }

    responses: dict = {
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
    }

    @staticmethod
    def load_user(instance: "DB" = None) -> dict:
        if not instance:
            instance = DB
        return {
            "access_token": instance.access_token,
            "me_token": instance.me_token,
            "secret": instance.secret,
            "responses": instance.responses,
            "lp_settings": instance.lp_settings,
            "settings": instance.settings,
            "trusted_users": instance.trusted_users,
            "chats": instance.chats,
            "templates": instance.templates,
            "voices": instance.voices,
            "anims": instance.anims
        }


class DB_general:
    'БД с основной информацией'
    path: str = path
    general: dict = {}
    owner_id: int = 0
    host: str = ""
    installed: bool = False
    vk_app_id: int = 0
    dc_auth: bool = False
    vk_app_secret: str = ""
    group_id = -195759899

    def __init__(self):
        logger.debug('Инициализация основной БД')
        self.general = read('general')
        self.general['dc_auth'] = self.general.get('dc_auth', False)
        self.__dict__.update(self.general)

    @property
    def update_general(self):
        'Обновляет экземпляр основной БД в файле database.py'
        global db_gen
        db_gen = DB_general()

    def set_user(self, user_id: int):  # TODO: гавной воняет
        if user_id == self.owner_id:
            raise ExcDB(1)
        self.owner_id = user_id
        with open(os.path.join(path, f'{user_id}.json'), "w", encoding="utf-8") as file:
            file.write(json.dumps(DB_defaults.load_user(),
                                  ensure_ascii=False, indent=4))
        self.save()
        self.update_general
        return DB(user_id)

    def save(self) -> str:
        'Сохранение основной БД'
        logger.debug("Сохраняю основную базу данных")
        for key in self.general:
            self.general[key] = getattr(self, key)
        with open(os.path.join(path, 'general.json'), "w", encoding="utf-8") as file:
            file.write(json.dumps(self.general, ensure_ascii=False, indent=4))
        self.update_general
        return "ok"


class DB:
    'БД для конкретного пользователя'
    gen: DB_general

    access_token: str = "Не установлен"
    me_token: str = "Не установлен"
    secret: str = ""
    chats: dict = {}
    trusted_users: List[int] = []
    duty_id: int = 0
    templates: List[dict] = []
    anims: List[dict] = []
    voices: List[dict] = []
    responses: dict = DB_defaults.responses

    settings: dict = DB_defaults.settings
    lp_settings: dict = DB_defaults.lp_settings

    def __init__(self, user_id: int = None):
        user_id = user_id or db_gen.owner_id
        if user_id != db_gen.owner_id:
            raise ExcDB(0)
        self.gen = db_gen
        self.duty_id = int(db_gen.owner_id)
        self.host = db_gen.host
        self.installed = db_gen.installed
        self.vk_app_id = db_gen.vk_app_id
        self.vk_app_secret = db_gen.vk_app_secret
        self.load_user()

    def load_user(self):
        try:
            user_db = read(str(self.duty_id))
        except FileNotFoundError:
            raise ExcDB(0)
        self.__dict__.update(user_db)

    def save(self) -> str:
        'Сохраняет БД пользователя, которая открыта в данном экземпляре DB'
        logger.debug("Сохраняю базу данных")
        with open(os.path.join(path, f'{str(self.duty_id)}.json'), "w", encoding="utf-8") as file:
            file.write(json.dumps(DB_defaults.load_user(self), ensure_ascii=False, indent=4))
        return "ok"


def _update(data):
    data['voices'] = []
    for i, temp in enumerate(data['templates']):
        data['templates'][i]['name'] = temp['name'].lower()
        data['templates'][i]['cat'] = temp['cat'].lower()
        if temp['attachments']:
            if temp['attachments'][0].startswith('audio_message'):
                data['voices'].append(temp)
                data['templates'][i]['payload'] = None
    for temp in data['templates']:
        if temp['payload'] is None:
            data['templates'].remove(temp)
    for i, temp in enumerate(data['dyntemplates']):
        data['dyntemplates'][i]['name'] = temp['name'].lower()
    if 'dyntemplates' in data:
        data['anims'] = data.pop('dyntemplates', [])
    with open(os.path.join(path, f'{db_gen.owner_id}.json'), "w", encoding="utf-8") as file:
        file.write(json.dumps(data, ensure_ascii=False, indent=4))


DB_general().update_general  # инициализация основной БД при запуске скрипта

# форматирование старых жысонов под новый формат
if db_gen.owner_id != 0:
    data = read(db_gen.owner_id)
    if 'dyntemplates' in data:
        try:
            _update(data)
        except Exception:
            pass
    if 'lp_settings' not in data:
        data['lp_settings'] = {

        }
    del(data)
