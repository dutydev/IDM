from duty.objects import dp


@dp.event_register('ping')
def ping(event) -> str:
    try:
        __import__('uwsgi').reload()
    except ImportError:
        pass
    return "ok"
