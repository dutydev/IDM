from ..objects import dp, Event, MySignalEvent
import typing

@dp.event_handle(dp.Methods.SEND_MY_SIGNAL)
def send_my_signal(event: Event) -> typing.Union[str, dict]:

    msevent = MySignalEvent(event)
    data = [d for d in dp.my_signal_event_run(msevent)]

    for d in data:
        if d != "ok":return d
    return "ok"