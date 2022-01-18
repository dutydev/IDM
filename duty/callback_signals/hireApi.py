from duty.objects import dp, Event


@dp.event_register('hireApi')
def hire(event: Event) -> str:
        return {"response":"ok","days":event.obj['price']}