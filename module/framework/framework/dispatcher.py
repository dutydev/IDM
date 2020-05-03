import asyncio
import typing
import traceback
import sys

from module.utils import LoggerLevel, logger
from module.utils import generate_string
from module.objects.events import Event
from module.framework.framework.bot import User
from module.framework.processor import AsyncHandleManager
from module.framework.error_handler import ErrorHandler
from module.framework.framework.blueprint import Blueprint
from vbml import Patcher
from vkbottle.framework.framework.handler.user import Handler
from dutymanager.units.const import errors

Token = typing.Union[str, list]


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
        patcher: Patcher = None,
        debug: typing.Union[str, bool] = True,
        errors_log: bool = False
    ):
        self._secret: str = secret or generate_string()
        self._user_id: int = user_id
        self._tokens = [tokens] if isinstance(tokens, str) else tokens

        self._debug: bool = debug
        self._patcher = patcher or Patcher()
        Patcher.set_current(self._patcher)

        self.__loop = asyncio.get_event_loop()
        self.__user: User = User(
            tokens=self._tokens, user_id=user_id,
            login=login, password=password,
            expand_models=len(self._tokens) > 1
        )
        if not secret:
            print(f"Generated new secret word: {self._secret}")

        if user_id is None:
            self._user_id = self.__user.user_id

        if isinstance(debug, bool):
            debug = "INFO" if debug else "ERROR"

        if polling:
            self.__loop.create_task(self.__user.run())

        self.logger = LoggerLevel(debug)
        self.on: Handler = self.__user.on
        self.event: Event = Event()
        self.error_handler: ErrorHandler = ErrorHandler()

        logger.remove()
        logger.add(
            sys.stderr,
            colorize=True,
            format="<blue>[IDM]</blue> <lvl>{message}</lvl> <white>[TIME {time:HH:MM:ss}]</white>",
            filter=self.logger,
            level=0,
            enqueue=mobile is False
        )
        logger.level("DEBUG", color="<white>")
        if errors_log:
            logger.add(
                "logs/errors.log",
                level="ERROR",
                format="[{time:YYYY-MM-DD HH:MM:SS +08:00} | {level}]: {message}",
                rotation="5 MB"
            )

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
            if task is not None:
                return task
        except Exception as e:
            processing = await self.error_processor(e)
            if processing is False:
                logger.exception(traceback.format_exc(limit=5))
                return traceback.format_exc(limit=5)

        return {"response": "ok"}

    def set_blueprints(self, *blueprints: Blueprint):
        for bp in blueprints:
            bp.create(self.api, self._user_id)
            self.event.concatenate(bp.event)
            self.error_handler.update(bp.error_handler.processors)
            self.on.concatenate(bp.on)
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