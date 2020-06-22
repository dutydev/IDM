from ..objects import dp, Event

@dp.event_handle('meetChatDuty')
def meet_chat_duty(event: Event) -> str:
    return "ok" #надо сюда че нить придумать