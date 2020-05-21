from dutymanager.files.config import MODELS_PATH, DB_URL
from module.utils.context import ContextInstanceMixin
from tortoise import Tortoise
from .abc import AbstractDict
from .standard import *


class AsyncDatabase(ContextInstanceMixin):
    def __init__(self):
        self.chats = Chats()
        self.trusted = Proxies()
        self.templates = Templates()

        self.settings = Settings()
        self.tokens = Tokens()
        self.pages = dict()

    def create_pages(self, limit: int = None):
        limit = limit or self.settings()
        current = 1
        self.pages.clear()
        tags = list(self.templates)
        for i in range(0, len(tags), limit):
            self.pages[current] = tags[i: i + limit]
            current += 1

    async def init(self):
        await Tortoise.init(
            db_url=DB_URL,
            modules={"models": [MODELS_PATH]}
        )
        await Tortoise.generate_schemas()
        await self.compose()

    async def compose(self):
        await AbstractDict.load()
        print(self.chats)
        try:
            self.create_pages()
        except KeyError:
            await self.settings.create()


db = AsyncDatabase()
AsyncDatabase.set_current(db)