from dutymanager.units.dataclasses.generator import Generator
from dutymanager.units.dataclasses.validator import patcher
from dutymanager.units.dataclasses.workers import worker
from module.utils.context import ContextInstanceMixin
from dutymanager.files.dicts import default_data
from dutymanager.units.tools import get_values
from dutymanager.web import web_blueprints
from module import Dispatcher, TaskManager
from dutymanager.plugins import blueprints
from dutymanager.files.const import Token
from dutymanager.db.methods import db
from dutymanager import setup_web
from pyinstrument import Profiler
from module.utils import logger
from typing import Union
from aiohttp import web

profiler = Profiler()

try:
    from pyngrok import ngrok
except ModuleNotFoundError:
    ngrok = None


class Core(ContextInstanceMixin):
    def __init__(
        self,
        *,
        secret: str = None,
        user_id: int = None,
        tokens: Token = None,
        login: str = None,
        password: str = None,
        polling: bool = False,
        mobile: bool = False,
        debug: Union[str, bool] = True,
        errors_log: bool = False,
    ):
        # Main workers
        self.bot = Dispatcher(**self.get_params(locals()), patcher=patcher)
        self.bot.api.token_generator = Generator(**get_values(Generator))
        self.app = web.Application()
        self.task = TaskManager(self.bot.loop)
        setup_web(self)

        # Sign assets
        self.bot.set_blueprints(*blueprints)
        self.bot.set_web_blueprints(*web_blueprints)
        self.app.router.add_route("POST", "/", self.wrapper)
        self.port = default_data.get("port", 8080)

    async def wrapper(self, request: web.Request):
        profiler.start()
        event = await request.json()
        emulation = await self.bot.emulate(event)
        profiler.stop()
        logger.debug(profiler.output_text(unicode=True, color=True))
        if isinstance(emulation, str):
            return web.Response(text=emulation)
        return web.json_response(data=emulation)

    def run(self, use_ngrok: bool = False):
        if use_ngrok:
            url = self.get_url(self.port)
            print("Using ngrok WSGI: {}", url)
        worker.dispatch(self.bot.loop)
        self.task.add_task(web._run_app(self.app, port=self.port))  # noqa
        self.task.add_task(db.init)
        self.task.run()

    @staticmethod
    def get_url(port: int) -> str:
        if ngrok is None:
            raise ModuleNotFoundError(
                "First install pyngrok - pip install pyngrok"
            )
        return ngrok.connect(port=port)