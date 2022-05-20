import requests
import traceback
from duty.objects import dp, MySignalEvent



@dp.longpoll_event_register('ип', 'айпи')
@dp.my_signal_event_register('ип', 'айпи')
def get_info_by_ip(event: MySignalEvent) -> str:
    ip = " ".join(event.args)
    if not ip:
        event.msg_op(2, "❗ Нет указан ip/домен")
    else:
        try:
            response = requests.get(url=f'http://ip-api.com/json/{ip}?lang=ru').json()

            if response.get("status") == "fail":
                data = "❌Информация не найдены. Проверьте данные"
            else:
                data = f'''
                ⚙Айпи чекер⚙
        
                🔎IP: {response.get('query')}
                🤖Провайдер: {response.get('isp')}
                🌇Страна: {response.get('country')}
                🏙Регион: {response.get('regionName')}
                🏙Город: {response.get('city')}
                🔑Индекс: {response.get('zip') if response.get('zip') != "" else "Не найдено"}
                ✏Координаты: {response.get('lat')}:{response.get('lon')}'''.replace("                ", "")
            event.msg_op(2, f'{data}')
        except Exception:
            print(traceback.format_exc())
    return "ok"
