from aiohttp import web
from jinja2 import Environment, FileSystemLoader
from dutymanager.units import const
from module.utils import DotDict

enviroment = Environment(
    loader=FileSystemLoader(const.TEMPLATES_PATH)
)

class LoginForm:

    template_name = 'forms/login.html'

    login: str
    password: str

    errors: DotDict = DotDict(
        form=[],
        login=[],
        password=[]
    )

    def __init__(self, post: 'MultiDictProxy[Union[str, bytes, FileField]]' = {}):
        self.login = post.get('login', None) if post else None
        self.password = post.get('password', None) if post else None

    def __html__(self):
        template = enviroment.get_or_select_template(self.template_name)
        return template.render(
            context={
                "login": self.login or "",
                "password": "",
                "errors": self.errors
            }
        )

    def validate(self):
        is_valide = True
        if not self.login:
            self.errors.login.append("Пустой логин")
            is_valide = False
        if not self.login:
            self.errors.login.append("Пустой пароль")
            is_valide = False
        return is_valide

