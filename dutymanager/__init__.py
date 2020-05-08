from dutymanager.web.context_processors import auth_user_ctx_processor
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
            auth_user_ctx_processor,
            aiohttp_jinja2.request_processor
        ]
    )
    self.app.router.add_static(
        STATIC_URL, STATIC_PATH,
        follow_symlinks=True
    )
    for url in urls.urlpatterns:
        url.register(self.app.router)