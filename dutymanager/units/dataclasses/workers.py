from dutymanager.units.vk_script import friends_method
from dutymanager.files.dicts import workers_state
from dutymanager.units.utils import get_requests
from asyncio import AbstractEventLoop, sleep
from module.utils import logger
from module import Blueprint

bot = Blueprint(name="Worker")


class Worker:
    """
    TODO: Recreate worker class.
    """

    def __init__(self, loop: AbstractEventLoop = None):
        self.metadata = {
            "online": self.online,
            "friends": self.friends,
            "deleter": self.deleter
        }
        self.loop = loop

    def dispatch(self):
        for k, v in self.metadata.items():
            if workers_state[k]:
                self.loop.create_task(v())
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
