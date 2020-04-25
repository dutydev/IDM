from module import Dispatcher, TaskManager
from tortoise import Tortoise
from aiohttp import web
from dutymanager.plugins import blueprints
from dutymanager.core.config import default_data
from dutymanager.db.methods import db
from dutymanager.units.dataclasses.workers import Worker
from dutymanager.units.tools import *
from dutymanager.units.dataclasses.validator import patcher


class Bot:
    def __init__(self):
        load_values()
        self.app = web.Application()
        self.bot = Dispatcher(**get_params(), patcher=patcher)
        self.bot.set_blueprints(*blueprints)
        self.task = TaskManager(self.bot.loop)
        self.worker = Worker(self.bot.loop)

    def start(self):
        self.app.router.add_route("POST", "/", self.wrapper)
        self.task.add_task(web._run_app(self.app, port=default_data["port"]))
        self.worker.start()
        self.task.run(on_startup=self.init)

    async def wrapper(self, request: web.Request):
        event = await request.json()
        emulation = await self.bot.emulate(event)
        if isinstance(emulation, str):
            return web.Response(text=emulation)
        return web.json_response(data=emulation)

    async def init(self):
        await Tortoise.init(
            db_url="sqlite://dutymanager/core/duty.db",
            modules={"models": ["dutymanager.db.models"]}
        )
        await Tortoise.generate_schemas()
        await db.load_values()
