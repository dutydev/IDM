from dutymanager.web.middlewares.errors import setup as setup_errors
from dutymanager.web.middlewares.logging import setup as setup_logging

__all__ = (
    'setup_errors',
    'setup_logging',
    'setup_all'
)


def setup_all(app):
    setup_logging(app)
    setup_errors(app)

