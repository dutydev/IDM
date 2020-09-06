# не хочу об этом разговаривать...
import re
from ..objects import DB
from microvk import VkApi
from .utils import parseByID, parse
from wtflog import warden

logger = warden.get_boy('Обработчик команд LP')


class ND:
    update: list

    db: DB
    vk: VkApi
    time: float
    msg: dict

    def __init__(self, update, db, vk, time, msg):
        self.update = update
        self.db = db
        self.vk = vk
        self.time = time
        self.msg = msg

    def __getitem__(self, key):
        return self.update[key]

    def __setitem__(self, key, value):
        self.update[key] = value



class DriverLP:
    commands_functions : dict = {}
    commands_list: set = set()
    commands_startswith: list = []
    commands_regulars: list = []
        

    def register(self, *args):
        '''Присваивает декорируемой функции указанную команду\n
        Выполняется, если сообщение полностью соответствует команде'''
        logger.debug(f'Зарегистрирована новая функция. Команды: ({args})')
        def registrator(command):
            for arg in args:
                self.commands_functions.update({arg: command})
                self.commands_list.add(arg)
            return command
        return registrator

    def register_startswith(self, *args):
        '''Присваивает декорируемой функции указанную команду\n
        Выполняется, если сообщение начинается с команды'''
        logger.debug(f'Зарегистрирована новая функция. Команды: ({args})')
        def registrator(command):
            for arg in args:
                self.commands_functions.update({arg: command})
                self.commands_startswith.append(arg)
            return command
        return registrator

    def register_regexp(self, regular, name):
        '''Присваивает декорируемой функции указанную команду\n
        Выполняется, если сообщение полностью соответствует регулярному выражению'''
        logger.debug(f'Зарегистрирована новая функция {name}. Регулярка: ({regular})')
        def registrator(command):
            self.commands_functions.update({name: command})
            self.commands_regulars.append({'name': name, 'reg': regular})
            return command
        return registrator


    def launch(self, update, db, vk, time, msg = 0):
        'Запускает выполнение команды, если она есть в списке зарегистрированных'
        nd = ND(update, db, vk, time, parse(msg, True) if msg else 0)
        name = nd.msg['command']
        logger(f'Выполняю команду "{name}"')
        if name in self.commands_list:
            return self.commands_functions[name](nd)

        for command in self.commands_startswith:
            if name.startswith(command):
                if not nd.msg:
                    nd.msg = parseByID(update[1], True)
                return self.commands_functions[command](nd)

        for command in self.commands_regulars:
            if re.fullmatch(command['reg'], name):
                return self.commands_functions[command['name']](nd)

        return f'Команда "{command}" не обнаружена'


dlp = DriverLP()
