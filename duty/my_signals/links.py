import requests
import traceback
from duty.objects import dp, MySignalEvent



@dp.longpoll_event_register('сс', 'сс')
@dp.my_signal_event_register('сс', 'сс')
def ssilka(event: MySignalEvent) -> str:
	ss = " ".join(event.args)
	try:
		url = requests.get(f'https://api.vk.com/method/utils.getShortLink?&v=5.131&url={ss}&access_token={event.db.me_token}')
		response__json = url.json()['response']['key']
		requests.get(f"https://api.vk.com/method/utils.deleteFromLastShortened?&v=5.131&key={response__json}&access_token={event.db.me_token}")
		event.msg_op(2, f'⚙ Ваша ссылка: vk.cc/{response__json}')
	except Exception:
		print(traceback.format_exc())
	return "ok" 

@dp.longpoll_event_register('-сс', '-сс')
@dp.my_signal_event_register('-сс', '-сс')
def checkLink(event: MySignalEvent) -> str:
	ss = ss = " ".join(event.args)
	try:
		url = requests.get(f'https://api.vk.com/method/utils.checkLink?&v=5.131&url={ss}&access_token={event.db.me_token}')
		response__json = url.json()['response']['link']
		event.msg_op(2, f'⚙ Ваша ссылка: {response__json}')
	except Exception:
		print(traceback.format_exc())
	return "ok" 