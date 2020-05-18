import wtforms
from jinja2 import Environment, FileSystemLoader
from wtforms import validators

from dutymanager.files.config import TEMPLATES_PATH
from dutymanager.web.objects import WebBlueprint
from dutymanager.web.utils import get_user

environment = Environment(
    loader=FileSystemLoader(TEMPLATES_PATH)
)

bot = WebBlueprint()


class LoginForm(wtforms.Form):
    user: dict

    login = wtforms.StringField(
        'Логин',
        validators=[validators.input_required()],
        render_kw={
            'class': 'form-control'
        }
    )

    password = wtforms.PasswordField(
        'Пароль',
        validators=[validators.input_required()],
        render_kw={
            'class': 'form-control'
        }
    )

    async def validate(self, extra_validators=None):
        self.user = await get_user(self.data['login'])
        if self.user['id'] != bot.user_id or self.data['password'] != bot.secret:
            self.errors.setdefault(
                '__all__',
                []
            ).append({
                'message': 'Не верный логин/пароль',
            })
            return False

        return super().validate(extra_validators)

    def set_user(self, obj: dict):
        obj.update(**self.user)
