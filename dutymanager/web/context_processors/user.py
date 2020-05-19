from typing import Dict, Any

from aiohttp import web

from dutymanager.web.auth import auth

__all__ = (
    'user_ctx',
)


async def user_ctx(request: web.Request) -> Dict[str, Any]:
    await auth.update(request)
    return {
        'user': {
            'is_anonymous': auth.is_anonymous(request),
            'is_authenticated': auth.is_authenticated(request),
            'info': auth.get_user()
        }
    }
