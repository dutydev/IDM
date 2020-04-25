import asyncio
import typing
import traceback
import sys

from module.utils import LoggerLevel, logger
from module.utils import generate_string
from module.objects.events import Event
from module.objects.methods import Method
from module.objects import types

from module.framework.processor import AsyncHandleManager
from module.framework.framework.blueprint import Blueprint
from vbml import Patcher
from vkbottle.user import User
from vkbottle import VKError
from const import errors


class Dispatcher(AsyncHandleManager):
    def __init__(
        self,
        secret: str = None,
        user_id: int = None,
        tokens: typing.Union[str, list] = None,
        login: str = None,
        password: str = None,
        polling: bool = False,
        mobile: bool = False,
        debug: typing.Union[str, bool] = True,
        log_to_path: typing.Union[str, bool] = False,
        patcher: Patcher = None,
        loop: asyncio.AbstractEventLoop = None,
    ):
        self._secret: str = secret or generate_string()
        self._user_id: int = user_id

        self._debug: bool = debug
        self._patcher = patcher or Patcher()

        self.__loop = loop or asyncio.get_event_loop()
        self.__user: User = User(
            tokens=tokens, login=login, password=password
        )
        if user_id is None:
            self._user_id = self.__user.user_id

        if isinstance(debug, bool):
            debug = "INFO" if debug else "ERROR"

        if polling:
            self.__loop.create_task(self.__user.run())

        self.logger = LoggerLevel(debug)
        self.on: Event = Event()

        logger.remove()
        logger.add(
            sys.stderr,
            colorize=True,
            format="<level>[<blue>Duty</blue>] {message}</level> <white>[TIME {time:HH:MM:ss}]</white>",
            filter=self.logger,
            level=0,
            enqueue=mobile is False
        )
        logger.level("INFO", color="<white>")
        logger.level("ERROR", color="<red>")
        if log_to_path:
            logger.add(
                "logs/log_{time}.log" if log_to_path is True else log_to_path,
                rotation="00:00",
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
            return errors[1]

        if event.get("secret") != self._secret:
            return errors[3]

        if event.get("user_id") != self._user_id:
            return errors[3]

        ev = await self.get_event_type(event)
        task = None
        try:
            task = (await self._processor(ev, self._patcher))
        except (VKError, Exception):
            logger.exception(traceback.format_exc())

        if task is not None:
            return {"response": task}

        return {"response": "ok"}

    def set_blueprints(self, *blueprints: Blueprint):
        for blueprint in blueprints:
            blueprint.api = self.api
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

    @staticmethod
    async def get_event_type(event: dict):
        """ What the bullshit I made...
        :param event: -> dict
        :return: object
        """
        event_type = Method(event["method"])
        ev = None
        if event_type is Method.PING:
            ev = types.Ping(**event)

        if event_type is Method.BIND_CHAT:
            ev = types.BindChat(**event)

        if event_type is Method.BAN_EXPIRED:
            ev = types.BanExpired(**event)

        if event_type is Method.ADD_USER:
            ev = types.AddUser(**event)

        if event_type is Method.IGNORE_MESSAGES:
            ev = types.IgnoreMessages(**event)

        if event_type is Method.SUBSCRIBE_SIGNALS:
            ev = types.SubscribeSignals(**event)

        if event_type is Method.DELETE_MESSAGES:
            ev = types.DeleteMessages(**event)

        if event_type is Method.DELETE_MESSAGES_FROM_USER:
            ev = types.DeleteMessagesFromUser(**event)

        if event_type is Method.PRINT_BOOKMARK:
            ev = types.PrintBookmark(**event)

        if event_type is Method.FORBIDDEN_LINKS:
            ev = types.ForbiddenLinks(**event)

        if event_type is Method.SEND_SIGNAL:
            ev = types.SendSignal(**event)

        if event_type is Method.SEND_MY_SIGNAL:
            ev = types.SendSignal(**event)

        if event_type is Method.HIRE_API:
            ev = types.HireApi(**event)

        if event_type is Method.BAN_GET_REASON:
            ev = types.BanGetReason(**event)

        if event_type is Method.TO_GROUP:
            ev = types.ToGroup(**event)

        return ev
