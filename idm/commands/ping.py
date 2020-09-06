from ..objects import dp


@dp.event_handle('ping')
def ping(event) -> str:
    return "ok"
