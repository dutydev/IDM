import typing
import os
import json
import logging

logger = logging.getLogger(__name__)


class DB:
    path: str

    access_token: str
    online_token: str
    me_token: str
    bp_token: str
    secret: str
    chats: str
    trusted_users: list
    owner_id: int 
    duty_id: int
    vk_app_id: int
    vk_app_secret: str
    templates: typing.List[dict]
    dynamic_templates: list

    host: str
    installed: bool

    def __init__(self):
        get_dir = os.path.dirname
        self.path = os.path.join(get_dir(get_dir(get_dir(__file__))), 'database.json')
        self.read()
        self.update()

    def update(self):
        self.__dict__.setdefault("dynamic_templates", [])
        self.save()

    def read(self):
        logger.debug("Читаю базу данных")
        with open(self.path, "r", encoding="utf-8") as file:
            self.__dict__.update(
                json.loads(file.read()))

    
    @property
    def raw(self) -> dict:
        return {
            "access_token": self.access_token,
            "online_token": self.online_token,
            "me_token": self.me_token,
            "bp_token": self.me_token,
            "secret": self.secret,
            "chats": self.chats,
            "trusted_users": self.trusted_users,
            "owner_id": self.owner_id,
            "duty_id": self.duty_id,
            "vk_app_id": self.vk_app_id,
            "vk_app_secret": self.vk_app_secret,
            "templates": self.templates,
            "dynamic_templates":self.dynamic_templates,
            "host": self.host,
            "installed": self.installed
        }

    def save(self) -> int:
        logger.debug("Сохраняю базу данных")
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.raw, ensure_ascii=False, indent=4))