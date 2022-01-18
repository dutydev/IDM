from duty.objects import dp, Event


@dp.event_register('meetChatDuty')
def meet_chat_duty(event: Event) -> str:
    return "ok"  # TODO: надо сюда че нить придумать
