from duty.objects import Event, ExceptToJson, dp
from microvk import VkApiResponseException
from logger import get_writer
from .app import app, DEBUG
from flask import request
import json

logger = get_writer('IRIS Callback')


@app.route('/callback', methods=["POST"])
def callback():
    event = Event(request)

    if event.secret != event.db.secret and not DEBUG:
        return 'Неверная секретка', 500

    d = dp.event_run(event)
    event.db.sync()
    if d is None:
        d = "ok"
    if d == "ok":
        return json.dumps({"response": "ok"}, ensure_ascii=False)
    elif type(d) == dict:
        return json.dumps(d, ensure_ascii=False)
    else:
        return r"\\\\\ашипка хэз бин произошла/////" + '\n' + d


@app.errorhandler(ExceptToJson)
def json_error(e):
    return e.response


@app.errorhandler(VkApiResponseException)
def vk_error(e: VkApiResponseException):
    return json.dumps({
        "response": "vk_error",
        "error_code": e.error_code,
        "error_message": e.error_msg
    }, ensure_ascii=False)
