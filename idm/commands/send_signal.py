from ..objects import dp, Event, SignalEvent

@dp.event_handle(dp.Methods.SEND_SIGNAL)
def send_signal(event: Event):

    sevent = SignalEvent(event)
    data = dp.signal_event_run(sevent)

    for d in data:
        if d != "ok":return "ok"
    return "ok"