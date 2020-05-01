from tortoise import Model


class AbstractDict(dict):

    dataclass: Model

    def __call__(self, *args):
        ...

    async def create(self, *args):
        ...

    async def remove(self, *args):
        ...

    async def change(self, **kwargs):
        ...