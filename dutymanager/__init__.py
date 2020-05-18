from dutymanager.web import context_processors, middlewares
from jinja2.loaders import FileSystemLoader
from dutymanager.web import urls
from dutymanager.files.config import (
    TEMPLATES_PATH,
    STATIC_PATH,
    STATIC_URL
)

import aiohttp_jinja2


def setup_web(self):
    aiohttp_jinja2.setup(
        self.app,
        loader=FileSystemLoader(TEMPLATES_PATH),
        context_processors=[
            context_processors.user_ctx,
            aiohttp_jinja2.request_processor
        ]
    )

    middlewares.setup_errors(self.app)
    middlewares.setup_auth(self.app)

    self.app.router.add_static(
        STATIC_URL, STATIC_PATH,
        follow_symlinks=True
    )
    for url in urls.urlpatterns:
        url.register(self.app.router)