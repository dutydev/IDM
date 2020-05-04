from module import Dispatcher, TaskManager
from tortoise import Tortoise
from aiohttp import web
from dutymanager.plugins import blueprints
from dutymanager.core.config import default_data
from dutymanager.db.methods import db
from dutymanager.units.dataclasses.workers import Worker
from dutymanager.units.dataclasses.validator import patcher
from dutymanager.units.tools import *
from dutymanager.web import urls
from jinja2.loaders import FileSystemLoader
from dutymanager.units import const
from dutymanager.web import blueprints as web_blueprints

import aiohttp_jinja2
from dutymanager.web.context_processors import auth_user_ctx_processor

try:
    from pyngrok import ngrok
except ModuleNotFoundError:
    ngrok = None

bot = Dispatcher(**get_params(), patcher=patcher)
bot.set_blueprints(*blueprints)
bot.set_web_blueprints(*web_blueprints)

task = TaskManager(bot.loop)
worker = Worker(bot.loop)


class Core:
    def __init__(self):
        self.app = web.Application()
        self.app.router.add_route("POST", "/", wrapper)
        self.port = default_data["port"]
        self.setup_web()

    def setup_web(self):
        aiohttp_jinja2.setup(
            self.app,
            loader=FileSystemLoader(const.TEMPLATES_PATH),
            context_processors=[
                auth_user_ctx_processor,
                aiohttp_jinja2.request_processor
            ]
        )
        self.app.router.add_static(
            const.STATIC_URL, const.STATIC_PATH,
            follow_symlinks=True
        )

        for url in urls.urlpatterns:
            url.register(self.app.router)

    def run(self, use_ngrok: bool = False):
        if use_ngrok:
            url = self.get_url()
            print("Using ngrok WSGI: {}", url)
        task.add_task(web._run_app(self.app, port=self.port))
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
