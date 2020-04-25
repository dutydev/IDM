"""

Configuration file

"""

default_data = {
    "access_token": None,
    "me_token": None,
    "online_token": None,
    "bp_token": None,
    "secret": None,
    "user_id": None,
    "debug": False,
    "port": 8080,
    "polling": False
}

intervals = {
    'г': 3.154e+7,
    'мес': 2.628e+6,
    'нед': 604800,
    'дн': 86400,
    'ч': 3600,
    'мин': 60,
    'сек': 1,
    'день': 86400
}

workers_state = {
    'online': False,
    'friends': False,
    'deleter': False
}

state = """[IDM v2.0]:
{}
Ответ через: {} сек"""