from module.utils.context import ContextInstanceMixin
from tortoise import Tortoise
from .standard import *


class AsyncDatabase(ContextInstanceMixin):
    def __init__(self):
        self.chats = Chats()
        self.trusted = Proxies()
        self.templates = Templates()
        self.settings = Settings()

        self.pages = dict()

    def create_pages(self, limit: int):
        current = 1
        self.pages.clear()
        tags = list(self.templates)
        for i in range(0, len(tags), limit):
            self.pages[current] = tags[i: i + limit]
            current += 1

    async def init(self):
        await Tortoise.init(
            db_url="sqlite://dutymanager/core/duty.db",
            modules={"models": ["dutymanager.db.models"]}
        )
        await Tortoise.generate_schemas()
        await self.load_values()

    async def load_values(self):
        async for i in Chat.all():
            self.chats[i.uid] = {
                "id": i.id, "title": i.title
            }

        async for x in Trusted.all():
            self.trusted[x.id] = x.name

        async for y in Template.all():
            self.templates[y.tag] = {
                "message": y.text,
                "attachment": y.attachments
            }
        async for z in Setting.all():
            self.settings["page_limit"] = z.page_limit
        self.create_pages(self.settings())


db = AsyncDatabase()
AsyncDatabase.set_current(db)