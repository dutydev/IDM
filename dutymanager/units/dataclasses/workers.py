from dutymanager.core.config import default_data, workers_state
from asyncio import AbstractEventLoop, sleep
from module.utils import logger
from module import Blueprint

import vk_api

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
        user = vk_api.VkApi(token=default_data["online_token"])
        while workers_state["online"]:
            await bot.api.account.set_online()
            await sleep(300)

    @staticmethod
    async def friends():
        user = vk_api.VkApi(token=default_data["bp_token"])
        while workers_state["friends"]:
            requests = user.method("friends.getRequests", {
                "count": 1000, "extended": 1
            })
            with vk_api.VkRequestsPool(user) as p:
                for i in requests["items"]:
                    if "deactivated" not in i:
                        p.method("friends.add", {
                            "user_id": i["user_id"],
                            "follow": 0
                        })
            await sleep(120)

    @staticmethod
    async def deleter():
        user = vk_api.VkApi(token=default_data["bp_token"])
        while workers_state["deleter"]:
            requests = user.method("friends.getRequests", {
                "count": 1000, "out": 1
            })
            with vk_api.VkRequestsPool(user) as p:
                for i in requests["items"]:
                    p.method("friends.delete", {"user_id": i})

            await sleep(3600)