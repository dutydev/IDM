"""

Built-in dictionaries

"""

default_data = {
    "tokens": None,
    "me_token": None,
    "online_token": None,
    "friends_token": None,
    "secret": None,
    "user_id": None,
    "debug": True,
    "errors_log": True,
    "port": 8080,
    "polling": False,
    "setup_mode": True,
}

intervals = {
    "год": 3.154e+7,
    "месяц": 2.628e+6,
    "неделя": 604800,
    "день": 86400,
    "час": 3600,
    "минута": 60,
    "секунда": 1,

    "г": 3.154e+7,
    "мес": 2.628e+6,
    "нед": 604800,
    "дн": 86400,
    "ч": 3600,
    "мин": 60,
    "сек": 1,
}

workers_state = {
    "online": False,
    "friends": False,
    "deleter": False
}
