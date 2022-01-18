
from duty.objects import dp, Event


@dp.event_register('forbiddenLinks')
def forbidden_links(event: Event) -> str:
    return "ok"
