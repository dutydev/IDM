import requests
import json
import os
import logging

from .exceptions import *
from enum import Enum

API_URL = "https://api.vk.com/method/"


class Mode(Enum):
    POST = "POST"
    GET = "GET"


class VkApi(object):

    def __init__(
        self,
        access_token: str,
        version: str = "5.103",
        mode: Mode = Mode.POST,
        lang: str = "ru",
        raise_excepts: bool = False
    ):

        self.logger = logging.getLogger('VKApi')
        self.raise_excepts = raise_excepts
        self.__access_token = access_token
        self.__mode = Mode(mode)
        self.__version = version
        self.__lang = lang

    def method(self, method: str, **kwargs):

        def load_methods():
            with open(os.path.join(os.path.dirname(__file__), "schemes", "methods.json")) as file:
                return json.loads(file.read())

        version = kwargs.get('version', self.__version)
        access_token = kwargs.get('access_token', self.__access_token)
        lang = kwargs.get('lang', self.__lang)
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

        if self.__mode is Mode.GET:
            url = f"{API_URL}{method}?"
            data_list = [f"{key_}={data[key_]}" for key_ in data.keys()]
            data_list.append(f"v={version}")
            data_list.append(f"access_token={access_token}")
            data_list.append(f"lang={lang}")

            url += "&".join(data_list)
            request = requests.get(url)

        else:
            url = f"{API_URL}{method}?v={version}&access_token={access_token}&lang={lang}"
            request = requests.post(url, data=data)

        if 'response' in request.json().keys():
            self.logger.info(f"Запрос {method} выполнен")
            return request.json()["response"]

        elif 'error' in request.json().keys():
            self.logger.info(f"Запрос {method} не выполнен: {request.json()['error']}")
            if raise_excepts:
                raise VkApiResponseException(**request.json()["error"])
            return request.json()

        raise Exception()

    def __call__(self, method, **kwargs):
        return self.method(method, **kwargs)
