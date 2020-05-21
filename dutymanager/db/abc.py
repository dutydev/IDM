from typing import List, TypeVar

T = TypeVar("T")


class AbstractDict(dict):

    sub_classes: List["AbstractDict"] = []

    def __init__(self):
        super().__init__()
        self.dataclass = None
        self.set_current(self)

    def __call__(self, *args):
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
            for x in await i.dataclass.all():
                i.update(x.load_model())
