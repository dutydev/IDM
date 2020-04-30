import asyncio
import typing
import traceback
import sys

from module.utils import LoggerLevel, logger
from module.utils import generate_string
from module.objects.events import Event
from module.framework.framework.bot import User
from module.framework.processor import AsyncHandleManager
from module.framework.framework.blueprint import Blueprint
from vbml import Patcher
from vkbottle.framework.framework.handler.user import Handler
from vkbottle import VKError
from dutymanager.units.const import errors

#  Type hints
Token = typing.Union[str, list]
Union = typing.Union[str, bool]


class Dispatcher(AsyncHandleManager):
    def __init__(
        self,
        secret: str = None,
        user_id: int = None,
        tokens: Token = None,
        login: str = None,
        password: str = None,
        polling: bool = False,
        mobile: bool = False,
        debug: Union = True,
        log_to_path: Union = False,
        patcher: Patcher = None,
        loop: asyncio.AbstractEventLoop = None,
    ):
        self._secret: str = secret or generate_string()
        self._user_id: int = user_id

        self._debug: bool = debug
        self._patcher = patcher or Patcher()

        self.__loop = loop or asyncio.get_event_loop()
        self.__user: User = User(
            tokens=tokens, user_id=user_id,
            login=login, password=password
        )
        if user_id is None:
            self._user_id = self.__user.user_id

        if isinstance(debug, bool):
            debug = "INFO" if debug else "ERROR"

        if polling:
            self.__loop.create_task(self.__user.run())

        # Sign assets
        self.logger = LoggerLevel(debug)
        self.on: Handler = self.__user.on
        self.event: Event = Event()

        logger.remove()
        logger.add(
            sys.stderr,
            colorize=True,
            format="<blue>[IDM]</blue> <lvl>{message}</lvl> <white>[TIME {time:HH:MM:ss}]</white>",
            filter=self.logger,
            level=0,
            enqueue=mobile is False
        )
        if log_to_path:
            logger.add(
                "logs/errors.log" if log_to_path is True else log_to_path,
                level=debug,
                format="[{time:YYYY-MM-DD HH:MM:SS} | {level}]: {message}",
                rotation="5 MB"
            )

        if not secret:
            logger.success("Generated new secret word: {}", self._secret)

    async def emulate(self, event: dict) -> typing.Union[dict, str]:
        """ Process all signals
        from IRIS CM.
        :param event: New signal
        :return: "ok" (if possible)
        """
        logger.debug("Event: {event}", event=event)

        if event is None:
            return {"response": "error", **errors[1]}

        if event.get("secret") != self._secret:
            return {"response": "error", **errors[3]}

        if event.get("user_id") != self._user_id:
            return {"response": "error", **errors[3]}

        try:
            task = (await self._processor(event))
        except (VKError, Exception):
            logger.exception(traceback.format_exc(limit=5))
            return traceback.format_exc(limit=5)

        if task is not None:
            return {"response": task}

        return {"response": "ok"}

    def set_blueprints(self, *blueprints: Blueprint):
        for blueprint in blueprints:
            blueprint.create(self.api, self._user_id)
            self.event.concatenate(blueprint.event)
            self.on.concatenate(blueprint.on)
        logger.debug("Blueprints have been successfully loaded")

    def loop_update(self, loop: asyncio.AbstractEventLoop = None):
        """ Update event loop
        :param loop: (Ignore it)
        :return: None
        """
        self.__loop = loop or asyncio.get_event_loop()
        return self.__loop

    @property
    def loop(self):
        return self.__loop

    @property
    def api(self):
        return self.__user.api

    @property
    def patcher(self):
        return Patcher.get_current()