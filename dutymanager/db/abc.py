from typing import List, TypeVar

T = TypeVar("T")


class AbstractDict(dict):

    sub_classes: List["AbstractDict"] = []

    def __init__(self):
        self.set_current(self)
        super(AbstractDict, self).__init__()

    def __call__(self, *args):
        ...

    async def load_values(self):
        ...

    async def create(self, *args):
        ...

    async def remove(self, *args):
        ...

    async def change(self, **kwargs):
        ...

    @classmethod
    def set_current(cls, value: T):
        cls.sub_classes.append(value)

    @classmethod
    async def load(cls):
        for i in cls.sub_classes:
            await i.load_values()