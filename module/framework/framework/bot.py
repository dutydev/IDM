import aiohttp
import traceback

from dutymanager.files.dicts import default_data
from module.utils import logger
from vkbottle.user import User as Bot

DEFAULT_WAIT: int = 25


class User(Bot):

    @property
    def stopped(self) -> bool:
        return self._stop

    @stopped.setter
    def stopped(self, value: bool):
        self._stop = value

    async def run(self, wait: int = DEFAULT_WAIT):
        self.__wait = wait
        logger.info("Polling will be started. Is it OK?")

        await self.get_server()
        self.on.dispatch()
        logger.debug("User Polling successfully started")

        while not self._stop:
            try:
                event = await self.make_long_request(self.long_poll_server)
                if isinstance(event, dict) and event.get("ts"):
                    self.__loop.create_task(self.emulate(event))
                    self.long_poll_server["ts"] = event["ts"]
                else:
                    await self.get_server()

            except (
                    aiohttp.ClientConnectionError,
                    aiohttp.ServerTimeoutError,
                    TimeoutError,
            ):
                # No internet connection
                logger.warning("Server Timeout Error!")

            except:
                logger.error(
                    "While user lp was running error occurred \n\n{}".format(
                        traceback.format_exc()
                    )
                )

        logger.error("Polling was stopped")
