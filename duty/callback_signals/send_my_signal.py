from duty.objects import dp, Event, MySignalEvent


@dp.event_register('sendMySignal')
def send_my_signal(event: Event):
    return dp.my_signal_event_run(MySignalEvent(event))
