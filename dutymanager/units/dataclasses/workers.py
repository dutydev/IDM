import asyncio
import vk_api
from module.utils import logger
from dutymanager.core.config import default_data, workers_state


class Worker:

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self.metadata = {
            "online": self.online,
            "friends": self.friends,
            "deleter": self.deleter
        }
        self.loop = loop or asyncio.get_event_loop()

    def start(self):
        for k, v in self.metadata.items():
            if workers_state[k]:
                self.loop.create_task(v())
        logger.debug("Workers have been dispatched.")

    @staticmethod
    async def online():
        user = vk_api.VkApi(token=default_data["online_token"])
        while workers_state["online"]:
            user.method("account.setOnline")
            await asyncio.sleep(300)

    @staticmethod
    async def friends():
        user = vk_api.VkApi(token=default_data["bp_token"])
        while workers_state["friends"]:
            requests = user.method("friends.getRequests", {
                "count": 1000, "extended": 1
            })["items"]
            with vk_api.VkRequestsPool(user) as p:
                for i in requests:
                    if "deactivated" not in i:
                        p.method("friends.add", {
                            "user_id": i["user_id"],
                            "follow": 0
                        })
            await asyncio.sleep(120)

    @staticmethod
    async def deleter():
        user = vk_api.VkApi(token=default_data["bp_token"])
        while workers_state["deleter"]:
            requests = user.method("friends.getRequests", {
                "count": 1000, "out": 1
            })["items"]
            with vk_api.VkRequestsPool(user) as p:
                for i in requests:
                    p.method("friends.delete", {"user_id": i})

            await asyncio.sleep(3600)