from dutymanager.web.objects import WebBlueprint
from aiohttp import web
from hashlib import md5

bot = WebBlueprint()

__all__ = (
    'get_user_hash', 'is_authenticated', 'is_anonymous'
)


def get_user_hash(user_id: int, user_secret: str) -> str:
    return md5(f"{user_id}{user_secret}".encode('utf-8')).hexdigest()


def is_authenticated(request: web.Request) -> bool:
    # hash is md5(uid + secret_code)
    _hash = request.cookies.get('hash', None)
    return _hash == get_user_hash(bot.user_id, bot.secret)


def is_anonymous(request: web.Request) -> bool:
    return not is_authenticated(request)
