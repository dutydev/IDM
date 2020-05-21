from .abc import AbstractDict
from .models import *
from typing import Union, List
from module.objects.enums import TokenType

__all__ = (
    'Chats', 'Chat',
    'Proxies', 'Trusted',
    'Templates', 'Template',
    'Setting', 'Settings',
    'Token', 'Tokens'
)

Type = Union[TokenType, str]


class Chats(AbstractDict):

    def __init__(self):
        super().__init__()
        self.dataclass = Chat

    def __call__(self, uid: str, field: str = "id") -> Union[str, int]:
        return self[uid][field]

    async def create(self, *args):
        uid, chat_id, title = args
        await Chat.create(uid=uid, id=chat_id, title=title)
        self[uid] = {"id": chat_id, "title": title}

    async def remove(self, uid: int) -> int:
        await Chat.filter(uid=uid).delete()
        return self.pop(uid)

    async def change(self, uid: int, **kwargs):
        await Chat.filter(uid=uid).update(**kwargs)
        self[uid].update(**kwargs)


class Templates(AbstractDict):

    def __init__(self):
        super().__init__()
        self.dataclass = Template

    def __call__(self, tag: str) -> dict:
        return self[tag.lower()]

    async def create(self, *args):
        tag, text, attachments = args
        save = await Template.create(
            tag=tag.lower(),
            text=text,
            attachments=attachments
        )
        self[save.tag] = {"message": text, "attachment": attachments}

    async def remove(self, tag: str):
        await Template.filter(tag=tag.lower()).delete()
        self.pop(tag.lower())

    async def change(self, tag: str, **kwargs):
        await Template.filter(tag=tag.lower()).update(**kwargs)
        self[tag.lower()].update(**kwargs)


class Proxies(AbstractDict):

    def __init__(self):
        super().__init__()
        self.dataclass = Trusted

    def __call__(self, uid: int) -> str:
        return self[uid]

    async def create_many(self, data: List[Trusted]) -> int:
        await Trusted.bulk_create(data)
        self.update({i.uid: i.name for i in data})
        return len(data)

    async def create(self, *args):
        uid, name = args
        await Trusted.create(uid=uid, name=name)
        self[uid] = name

    async def remove_many(self, ids: list) -> int:
        await Trusted.filter(uid__in=ids).delete()
        [self.pop(i) for i in ids]
        return len(ids)

    async def remove(self, uid: int):
        await Trusted.filter(id=uid).delete()
        self.pop(uid)

    async def change(self, *args):
        uid, name = args
        await Trusted.filter(uid=uid).update(name=name)
        self[uid] = name


class Settings(AbstractDict):

    def __init__(self):
        super().__init__()
        self.dataclass = Setting

    def __call__(self, tag: str = "page_limit") -> int:
        return self[tag]

    async def create(self, *args):
        if not await Setting.get_or_none(id=1):
            setting = await Setting.create()
            self["page_limit"] = setting.page_limit

    async def change(self, **kwargs):
        await Setting.filter(id=1).update(**kwargs)
        self.update(**kwargs)


class Tokens(AbstractDict):

    def __init__(self):
        super().__init__()
        self.dataclass = Token

    def __call__(self, *args, **kwargs):
        ...

    def create(self, *args):
        ...

    def change(self, **kwargs):
        ...

    def remove(self, *args):
        ...

