from ..objects import dp, Event, SignalEvent

@dp.event_handle('sendSignal')
def send_signal(event: Event):
    return dp.signal_event_run(SignalEvent(event))