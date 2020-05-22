"""

Templates for messages

"""

setup = """Дежурный запущен в режиме установки. 
Это значит, что он не будет доступен для приема сигналов, 
пока вы его не настроите.

Конфигурационная панель находится по этому адресу: {}"""

ping_state = """{}

Ответ через: {} сек.
Время сервера ВК: {}
Время сервера IDM: {}"""

info_state = """Информация о дежурном:
IDM v{}
Владелец: [id{}|{}]
Чатов: {}
Доверенных: {}

Клиент LongPoll: {}
Автодобавление в друзья: {}
Автоотписка: {}
Вечный онлайн: {}

Информация о чате:
Iris ID: {}
Локальный айди: {}
Имя: {}
"""