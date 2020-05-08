from dutymanager.files.config import TEMPLATES_PATH
from jinja2 import Environment, FileSystemLoader
from dutymanager.web.objects import WebBlueprint

environment = Environment(
    loader=FileSystemLoader(TEMPLATES_PATH)
)

bot = WebBlueprint()


class LoginForm:
    """
    TODO: Refactoring
    """
    template_name = 'forms/login.html'

    login: str
    password: str
    errors: dict

    def __init__(self, post: 'MultiDictProxy[Union[str, bytes, FileField]]' = None):
        self.login = post.get('login', None) if post else None
        self.password = post.get('password', None) if post else None
        self.errors = {
            "form": [],
            "login": [],
            "password": []
        }

    def __html__(self):
        template = environment.get_or_select_template(self.template_name)
        return template.render(
            **{
                "login": self.login or "",
                "password": "",
                "form_errors": self.errors
            }
        )

    def validate(self):
        is_valid = True

        if not self.login:
            self.errors['login'].append("Пустой логин")
            is_valid = False

        if not self.password:
            self.errors['password'].append("Пустой пароль")
            is_valid = False

        if self.login != str(bot.user_id) or self.password != bot.secret:
            self.errors['form'].append('Не верный логин/пароль')
            is_valid = False

        return is_valid
