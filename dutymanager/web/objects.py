from aiohttp import web
import typing


class WebBlueprint:

    def __init__(self):
        self.user_id: int = None
        self.secret: str = None

    def create(self, user_id: int, secret: str):
        self.user_id = user_id
        self.secret = secret


class UrlPath:
    def __init__(
        self,
        method: str,
        path: str,
        handler: typing.Callable,
        name: str = None
    ):
        self.method = method
        self.path = path
        self.handler = handler
        self.name = name

    @staticmethod
    def add_post(
        path: str,
        handler: typing.Callable,
        name: str = None
    ):
        return UrlPath('POST', path, handler, name)

    @staticmethod
    def add_get(
        path: str,
        handler: typing.Callable,
        name: str = None
    ):
        return UrlPath('GET', path, handler, name)

    def register(self, router: web.UrlDispatcher) -> web.AbstractRoute:
        return router.add_route(self.method, self.path, self.handler, name=self.name)
