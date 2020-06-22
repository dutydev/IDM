
from ..objects import dp, Event
from .. import utils
from microvk import VkApiResponseException

@dp.event_handle('forbiddenLinks')
def forbidden_links(event: Event) -> str:
    return "ok"