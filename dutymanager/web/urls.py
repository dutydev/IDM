import typing
from aiohttp import web
from dutymanager.web import viewers


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


urlpatterns = [
    UrlPath.add_get('', viewers.index, name='index'),
    UrlPath.add_get('/home', viewers.index),

    UrlPath.add_get('/login', viewers.login, name='login'),
    UrlPath.add_post('/login', viewers.login),
]
