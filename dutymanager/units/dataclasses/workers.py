from dutymanager.units.vk_script import friends_method
from dutymanager.files.dicts import workers_state
from dutymanager.units.utils import get_requests
from asyncio import AbstractEventLoop, sleep
from module.utils.context import ContextInstanceMixin
from module.utils import logger
from module import Blueprint

bot = Blueprint(name="Worker")


class Worker(ContextInstanceMixin):

    loop: AbstractEventLoop

    def __init__(self):
        self.metadata = {
            "online": self.online,
            "friends": self.friends,
            "deleter": self.deleter
        }

    def manage_worker(self, state: str, start: bool):
        workers_state[state] = start
        if start:
            self.loop.create_task(self.metadata[state]())
        logger.info(
            "Worker <{}> has been {}!",
            state, ("stopped", "started")[start]
        )

    def dispatch(self, loop: AbstractEventLoop):
        self.loop = loop
        for k, v in self.metadata.items():
            if workers_state[k]:
                loop.create_task(v())
        logger.debug("Workers have been dispatched.")

    @staticmethod
    async def online():
        while workers_state["online"]:
            await bot.api.account.set_online()
            await sleep(300)

    @staticmethod
    async def friends():
        while workers_state["friends"]:
            await friends_method([
                i["user_id"] for i in await get_requests()
                if "deactivated" not in i
            ])
            await sleep(120)

    @staticmethod
    async def deleter():
        while workers_state["deleter"]:
            await friends_method(
                await get_requests(out=True), add=False
            )
            await sleep(3600)


worker = Worker()
Worker.set_current(worker)