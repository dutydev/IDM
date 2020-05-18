from dutymanager.web.auth import bot as auth_bot
from dutymanager.web.forms import bot as forms_bot
from dutymanager.web.utils import bot as utils_bot

web_blueprints = (
    utils_bot,
    forms_bot,
    auth_bot,
)
