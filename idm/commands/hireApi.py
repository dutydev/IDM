from ..objects import dp, Event
from ..utils import new_message

@dp.event_handle('hireApi')
def hire(event: Event) -> str:
        return {"response":"ok","days":event.obj['price']}