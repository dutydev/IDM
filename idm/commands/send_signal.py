from ..objects import dp, Event, SignalEvent
import typing

@dp.event_handle(dp.Methods.SEND_SIGNAL)
def send_signal(event: Event) -> typing.Union[str, dict]:

    sevent = SignalEvent(event)
    data = [d for d in dp.signal_event_run(sevent)]

    for d in data:
        if d != "ok":return d
    return "ok"