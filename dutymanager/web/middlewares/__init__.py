from dutymanager.web.middlewares.auth import setup as setup_auth
from dutymanager.web.middlewares.errors import setup as setup_errors

__all__ = (
    'setup_errors',
    'setup_auth'
)
