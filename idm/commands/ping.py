from ..objects import dp, Event

@dp.event_handle(dp.Methods.PING)
def ping(event: Event) -> str:
    return "ok"