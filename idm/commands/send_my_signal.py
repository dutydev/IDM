from ..objects import dp, Event, MySignalEvent

@dp.event_handle(dp.Methods.SEND_MY_SIGNAL)
def send_my_signal(event: Event):

    msevent = MySignalEvent(event)
    data = dp.my_signal_event_run(msevent)

    for d in data:
        if d != "ok":return {'error':str(d)}
    return "ok"