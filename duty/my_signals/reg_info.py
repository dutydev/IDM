import requests
import datetime
from duty.objects import dp, MySignalEvent
from duty.utils import find_mention_by_event, format_push


@dp.longpoll_event_register('рег')
@dp.my_signal_event_register('рег')
def reg_info(event: MySignalEvent) -> str:
    uid = find_mention_by_event(event)
    if not uid:
        uid = event.db.owner_id
    user = event.api(
        'users.get',
        user_ids=uid,
        fields="last_name_abl,first_name_abl")[0]
    event.msg_op(2, f"👤 Пользователь {format_push(user)}\n{regday(uid)}")


def regday(uid):
    url = 'https://vk.com/foaf.php?id=' + str(uid)
    response = requests.get(url).text
    num = response.find('<ya:created')
    text = response[(num + 21):(num + 46)]
    dt = datetime.datetime.strptime(text[:19], '%Y-%m-%dT%H:%M:%S')
    dtn = datetime.datetime.utcnow()

    offset = datetime.timedelta(hours=int(text[21:22]))

    if text[19] == '+':
        dt -= offset
    elif text[19] == '-':
        dt += offset
    else:
        return "Ошибка"

    time = dtn - dt
    all_days = time.days
    secs = time.seconds
    years = round(all_days // 365.25)
    weeks = round(all_days % 365.25 // 7)
    days = round(all_days % 365.25 % 7)
    hours = round(secs // 3600)
    minutes = round(secs % 3600 // 60)
    seconds = round(secs % 3600 % 60)

    monr = round(all_days % 365.25 // 30.4375)
    dayr = round(all_days % 365.25 % 30.4375)
    msg = '''🗓 Аккаунт зарегистрирован: {} в {} (по МСК)\n🕛 Аккаунт существует примерно {} лет {} месяцев {} дней\n🕛 С точностью до секунд: {} лет {} недель {} дней\n{} часов {} минут {} секунд'''.format(
        dt.date(), dt.time(), years, monr, dayr, years, weeks, days, hours, minutes, seconds)
    return msg.replace('    ', "")
