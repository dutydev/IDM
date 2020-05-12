from module.objects.types import MeetChatDuty
from module import Blueprint

bot = Blueprint(name="MeetChatDuty")


@bot.event.meet_chat_duty()
async def meet_chat_duty(event: MeetChatDuty):
    """
    Новый сигнал IRIS CM.
    Приходит тогда, когда вы пытаетесь
    вернуться в беседу через команды
    "верни в {}" и "добавь в {}".

    P.S. Чтобы сигнал работал, вы не должны
    быть в друзьях у дежурного и сам дежурный
    должен вернуть ошибку:
    {"response": "error", "error_code": 15}
    """
    await bot.api.friends.add(
        user_id=event.object.duty_id,
        follow=False
    )