from module import Dispatcher, types
from module import Method
from aiohttp import web

bot = Dispatcher(
    login="", password="",
    debug="DEBUG", secret=""
)
app = web.Application()


async def wrapper(request: web.Request):
    event = await request.json()
    emulation = await bot.emulate(event)
    return web.json_response(data=emulation)


@bot.on.event(Method.HIRE_API)
async def hire_api(event: types.HireApi):
    print(event)


if __name__ == '__main__':
    app.router.add_route("POST", "/", wrapper)
    web.run_app(app, port=80)