from jinja2 import Environment, FileSystemLoader
from dutymanager.units import const

environment = Environment(
    loader=FileSystemLoader(const.TEMPLATES_PATH)
)


class LoginForm:
    """
    TODO: Refactoring
    """
    template_name = 'forms/login.html'

    login: str
    password: str

    errors: dict

    def __init__(self, post: 'MultiDictProxy[Union[str, bytes, FileField]]' = None):
        print(post)
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

        return is_valid
