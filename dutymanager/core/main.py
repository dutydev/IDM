from module import Dispatcher, TaskManager
from module.utils import logger
from tortoise import Tortoise
from aiohttp import web
from dutymanager.plugins import blueprints
from dutymanager.core.config import default_data
from dutymanager.db.methods import db
from dutymanager.units.dataclasses.workers import Worker
from dutymanager.units.tools import *
from dutymanager.units.dataclasses.validator import patcher

try:
    from pyngrok import ngrok
except ModuleNotFoundError:
    ngrok = None

bot = Dispatcher(**get_params(), patcher=patcher)
bot.set_blueprints(*blueprints)
task = TaskManager(bot.loop)
worker = Worker(bot.loop)


class Core:
    def __init__(self, use_ngrok: bool = False):
        self.use_ngrok = use_ngrok
        self.app = web.Application()
        self.app.router.add_route("POST", "/", wrapper)
        self.port = default_data["port"]

    def run(self):
        if self.use_ngrok:
            logger.info("Using ngrok WSGI: {}", self.get_url())
        task.add_task(web._run_app(self.app, port=self.port))  # noqa
        worker.start()
        task.run(on_startup=init)

    def get_url(self) -> str:
        if ngrok is None:
            raise ModuleNotFoundError(
                "First install pyngrok - pip install pyngrok"
            )
        return ngrok.connect(port=self.port)


async def wrapper(request: web.Request):
    event = await request.json()
    emulation = await bot.emulate(event)
    if isinstance(emulation, str):
        return web.Response(text=emulation)
    return web.json_response(data=emulation)


async def init():
    await Tortoise.init(
        db_url="sqlite://dutymanager/core/duty.db",
        modules={"models": ["dutymanager.db.models"]}
    )
    await Tortoise.generate_schemas()
    await db.load_values()
