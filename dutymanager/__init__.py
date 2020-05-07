from dutymanager.web.context_processors import auth_user_ctx_processor
from jinja2.loaders import FileSystemLoader
from dutymanager.files import const
from dutymanager.web import urls

import aiohttp_jinja2


def setup_web(self):
    aiohttp_jinja2.setup(
        self.app,
        loader=FileSystemLoader(const.TEMPLATES_PATH),
        context_processors=[
            auth_user_ctx_processor,
            aiohttp_jinja2.request_processor
        ]
    )
    self.app.router.add_static(
        const.STATIC_URL, const.STATIC_PATH,
        follow_symlinks=True
    )
    for url in urls.urlpatterns:
        url.register(self.app.router)