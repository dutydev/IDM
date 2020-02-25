from ..objects import dp, Event

@dp.event_handle(dp.Methods.IGNORE_MESSAGES)
def ignore_messages(event: Event) -> str:
    return "ok"