
import requests
import enum
import json
import os

from .exceptions import *

import logging



class Mode(enum.Enum):
    POST = "POST"
    GET = "GET"


class VkApi(object):
    Mode: Mode

    mode: Mode
    access_token: str
    version: str
    lang: str
    raise_excepts: bool
    api_url = "https://api.vk.com/method/"

    


    def __init__(self, access_token: str, version: str = "5.103", mode: Mode = Mode.POST, 
            lang: str = "ru", raise_excepts: bool = False):
        
        self.logger = logging.getLogger('vkapi')
        self.Mode = Mode
        self.access_token = access_token
        self.version = version
        self.mode = self.Mode(mode)
        self.lang = lang
        self.raise_excepts = raise_excepts

    def method(self, method, **kwargs):

        def load_methods():                        
            with open(os.path.join(os.path.dirname(__file__), "schemes", "methods.json")) as file:
                return json.loads(file.read()) 



        mode = self.Mode(kwargs.get('mode', self.mode))
        version = kwargs.get('version', self.version)
        access_token = kwargs.get('access_token', self.access_token)
        lang = kwargs.get('lang', self.lang)
        raise_excepts = kwargs.get('raise_excepts', self.raise_excepts)


        methods = [method__['name'].lower() for method__ in load_methods()['methods']]

        if method.lower() not in methods:
            if raise_excepts:
                raise InvalidMethodException(method)
            else:
                return [err for err in load_methods() if err['name'] == "API_ERROR_METHOD"][0]

        data = {}
        for key in kwargs.keys():
            if key.lower() not in ["mode", "version", "access_token", "lang", "raise_excepts"]:
                data[key] = kwargs[key]

        request = None

        if mode == self.Mode.GET:
            url_ = self.api_url + method + "?"
            data_list = [f"{key_}={data[key_]}" for key_ in data.keys()]
            data_list.append(f"v={version}")
            data_list.append(f"access_token={access_token}")
            data_list.append(f"lang={lang}")

            url_ += "&".join(data_list)
            request = requests.get(url_)

        else:
            url_ = self.api_url + method + f"?v={version}&access_token={access_token}&lang={lang}"
            request = requests.post(url_, data=data)

        if 'response' in request.json().keys():
            self.logger.info(f"Запрос {method} выполнен")
            return request.json()["response"]
        elif 'error' in request.json().keys():
            self.logger.info(f"Запрос {method} не выполнен: {request.json()['error']}")
            if raise_excepts:
                raise VkApiResponseException(**request.json()["error"])
            else:
                return request.json()
        else:
            raise Exception()

        

            



    def __call__(self, method, **kwargs):
        return self.method(method, **kwargs)