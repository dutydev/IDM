from idm.objects import dp


@dp.event_register('ping')
def ping(event) -> str:
    return "ok"
