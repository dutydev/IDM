from dutymanager.web.viewers import bot as viewers_bot
from dutymanager.web.utils import bot as utils_bot
from dutymanager.web.forms import bot as forms_bot
from dutymanager.web.context_processors import bot as context_processors_bot

web_blueprints = (
    viewers_bot, utils_bot,
    forms_bot, context_processors_bot,
)