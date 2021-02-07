from typing import Union

from vkapi import VkApiResponseException
from ..objects import dp, Event


@dp.event_handle(dp.Methods.MEET_CHAT_DUTY)
def meet_chat_duty(event: Event) -> Union[str, dict]:
    try:
        event.api.method(
            'friends.add',
            user_id=event.obj['duty_id']
        )
    except VkApiResponseException as ex:
        return {
            "response": "vk_error",
            "error_code": ex.error_code,
            "error_message": ex.error_msg
        }
    return {'response': 'ok'}
