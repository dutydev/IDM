from module import Dispatcher, TaskManager
from tortoise import Tortoise
from aiohttp import web
from dutymanager.plugins import blueprints
from dutymanager.db.methods import db
from dutymanager.units.tools import *
from dutymanager.units.validator import patcher

load_values()
bot = Dispatcher(**get_params(), patcher=patcher)
bot.set_blueprints(*blueprints)
task = TaskManager(bot.loop)


async def wrapper(request: web.Request):
    event = await request.json()
    emulation = await bot.emulate(event)
    return web.json_response(data=emulation)


async def init():
    await Tortoise.init(
        db_url="sqlite://duty.db",
        modules={"models": ["dutymanager.db.models"]}
    )
    await Tortoise.generate_schemas()
    await db.load_values()


if __name__ == '__main__':
    app = web.Application()
    app.router.add_route("POST", "/", wrapper)
    task.add_task(web._run_app(app, port=80))
    task.run(on_startup=init)