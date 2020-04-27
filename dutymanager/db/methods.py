from vkbottle.utils import ContextInstanceMixin
from .models import Chat, Trusted, Template


class AsyncDatabase(ContextInstanceMixin):
    def __init__(self):
        self.chats = dict()
        self.trusted = dict()
        self.templates = dict()

    async def create_chat(self, *args):
        uid, chat_id = args
        await Chat.create(uid=uid, id=chat_id)
        self.chats[uid] = chat_id

    async def remove_chat(self, uid: str) -> int:
        await Chat.filter(uid=uid).delete()
        return self.chats.pop(uid)

    async def create_trusted(self, *args):
        uid, name = args
        await Trusted.create(id=uid, name=name)
        self.trusted[uid] = name

    async def remove_trusted(self, uid: int) -> str:
        await Trusted.filter(id=uid).delete()
        return self.trusted.pop(uid)

    async def add_template(self, *args):
        tag, text, attachments = args
        await Template.create(
            tag=tag.lower(),
            text=text,
            attachments=attachments
        )
        self.templates[tag.lower()] = {
            "message": text,
            "attachment": attachments
        }

    async def edit_template(self, tag: str, *args):
        text, attachments = args
        self.templates[tag].update({
            "message": text,
            "attachment": attachments
        })
        await Template.filter(tag=tag).update(
            text=text, attachments=attachments
        )

    async def remove_template(self, tag: str) -> str:
        await Template.filter(tag=tag).delete()
        return self.templates.pop(tag)

    async def load_values(self):
        async for i in Chat.all():
            self.chats[i.uid] = i.id

        async for x in Trusted.all():
            self.trusted[x.id] = x.name

        async for y in Template.all():
            self.templates[y.tag] = {
                "message": y.text,
                "attachment": y.attachments
            }


db = AsyncDatabase()
AsyncDatabase.set_current(db)