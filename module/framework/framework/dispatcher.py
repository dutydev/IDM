import asyncio
import sys
import traceback
import typing

from vbml import Patcher
from vkbottle.framework.framework.handler.user import Handler

from dutymanager.files.const import Token
from dutymanager.units.tools import get_values
from dutymanager.web.objects import WebBlueprint
from module.framework.error_handler import ErrorHandler
from module.framework.framework.blueprint import Blueprint
from module.framework.framework.bot import User
from module.framework.processor import AsyncHandleManager
from module.objects.events import Event
from module.objects.enums import Method
from module.utils import LoggerLevel, logger
from module.utils import generate_string


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
        errors_log: bool = False,
    ):
        self.secret: str = secret or generate_string()
        self.user_id: int = user_id

        self._tokens = [tokens] if isinstance(tokens, str) else tokens
        self._debug: bool = debug
        self._patcher = patcher or Patcher(pattern="^{}$")
        if not Patcher.get_current():
            Patcher.set_current(self._patcher)

        if polling and len(self._tokens) < 2:
            raise RuntimeError(
                "Для работы LongPoll необходимы, как минимум 2 токена."
            )

        self.__loop = asyncio.get_event_loop()
        self.__user: User = User(**get_values(User, locals()))
        if not secret:
            print("Generated new secret word: ", self.secret)

        if user_id is None:
            self.user_id = self.__user.user_id

        if polling:
            self.run_polling()

        if isinstance(debug, bool):
            debug = "INFO" if debug else "CRITICAL"

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
                format="{time:YYYY-MM-DD HH:MM:ss} | {level} | {message}",
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
            return {"response": "error", "error_code": 1}

        if event["method"] not in Method.list():
            return {"response": "error", "error_code": 2}

        if not self._check_data(event["user_id"], event["secret"]):
            return {"response": "error", "error_code": 3}

        try:
            task = (await self._processor(event))
            return task or {"response": "ok"}
        except Exception as e:
            processing = await self.error_processor(e, event)
            if not processing:
                logger.error(traceback.format_exc(limit=5))
                return traceback.format_exc(limit=5)

            return processing

    def _check_data(self, user_id: int, secret: str) -> bool:
        return (self.secret, self.user_id) == (secret, user_id)

    def dispatch(self, other: "Blueprint"):
        self.on.concatenate(other.on)
        self.error_handler.update(other.error_handler.processors)
        self.__user.middleware.middleware += other.middleware.middleware

    def set_blueprints(self, *blueprints: Blueprint):
        for bp in blueprints:
            bp.create(self.api, self.user_id)
            self.event.concatenate(bp.event)
            self.dispatch(bp)
        logger.debug("Blueprints have been successfully loaded")

    def set_web_blueprints(self, *blueprints: WebBlueprint):
        for blueprint in blueprints:
            blueprint.create(self.api, self.user_id, self.secret)
        logger.debug("Web-Blueprints have been successfully loaded")

    def loop_update(self, loop: asyncio.AbstractEventLoop = None):
        """ Update event loop
        :param loop: (Ignore it)
        :return: None
        """
        self.__loop = loop or asyncio.get_event_loop()
        return self.__loop

    def run_polling(self):
        if not self.__user.stopped:
            raise RuntimeError(
                "Polling has been already started!"
            )
        self.__user.stopped = False
        self.loop.create_task(self.__user.run())

    @property
    def loop(self):
        return self.__loop

    @property
    def api(self):
        return self.__user.api

    @property
    def patcher(self):
        return Patcher.get_current()