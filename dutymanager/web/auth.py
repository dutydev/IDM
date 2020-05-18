from hashlib import md5
from typing import Union

from aiohttp import web

from dutymanager.web.objects import WebBlueprint
from dutymanager.web.utils import get_user

__all__ = (
    'bot',
    'auth'
)

bot = WebBlueprint()


class Auth:
    current_user = {}

    def get_user(self) -> dict:
        return self.current_user

    async def update(self, request: web.Request):
        if not self.current_user and self.is_authenticated(request):
            self.current_user = await get_user(f'id{bot.user_id}')

    def set_user(self, data: dict):
        self.current_user = data

    @staticmethod
    def get_user_hash(user_id: Union[int, str], user_secret: str) -> str:
        return md5(f"{user_id}{user_secret}".encode('utf-8')).hexdigest()

    def is_authenticated(self, request: web.Request) -> bool:
        # hash is md5(uid + secret_code)
        _hash = request.cookies.get('hash', None)
        return _hash == self.get_user_hash(bot.user_id, bot.secret)

    def is_anonymous(self, request: web.Request) -> bool:
        return not self.is_authenticated(request)


auth = Auth()
