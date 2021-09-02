"""
да, написать свой говнологгер мне проще, чем научиться использовать встроенный

а че?)
"""
# TODO: уменьшить говнистость
from datetime import datetime
import os

class Warden:
    path: str
    format_string: str = '%(time)s | %(level)s (%(name)s)'
    names: dict
    level: int
    printing: bool

    USELESS = 0
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5


    def setup(self, path, format_string: str = False, level: int = 2, name: str = '',
                printing: bool = False, clear_on_start: str = False):
        self.path = path
        if clear_on_start:
            self._clear_log(clear_on_start)
        self.level = level
        self.printing = printing
        if format_string:
            self.format_string = format_string
        return self.get_boy(name)
        
    def get_boy(self, name):# не надо меня спрашивать, почему оно так называется.
        return ErrandBoy(self, name)

    def format_log(self, text, name, level):
        time = datetime.now().replace(microsecond = 0)
        return f"{self.format_string % {'time': time, 'name': name, 'level': level}} {text}"

    def _clear_log(self, clear_on_start):
        if clear_on_start == 'backup':
            with open(self.path + '.backup', 'w', encoding='utf-8') as backup:
                try:
                    backup.write(open(self.path, 'r', encoding='utf-8').read())
                except:
                    pass
        try:
            os.remove(self.path)
        except:
            pass


class ErrandBoy:
    name: str
    warden: Warden


    def __init__(self, warden, name):
        self.warden = warden
        self.name = name

    def __call__(self, text):
        return self.info(text)

    def _write(self, line):
        with open(self.warden.path, 'a', encoding='utf-8') as log:
            log.write(line + '\n')
        if warden.printing or os.environ.get('FLASK_ENV') == 'development':
            print(line)


    def useless(self, text):
        if warden.level == 0:
            self._write(self.warden.format_log(text, self.name, 'USELESS SHIT'))

    def debug(self, text):
        if warden.level <= 1:
            self._write(self.warden.format_log(text, self.name, 'DEBUG'))

    def info(self, text):
        if warden.level <= 2:
            self._write(self.warden.format_log(text, self.name, 'INFO'))
        
    def warning(self, text):
        if warden.level <= 3:
            self._write(self.warden.format_log(text, self.name, 'WARNING'))

    def error(self, text):
        if warden.level <= 4:
            self._write(self.warden.format_log(text, self.name, 'ERROR'))

    def critical(self, text):
        if warden.level <= 5:
            self._write(self.warden.format_log(text, self.name, 'CRITICAL'))



warden = Warden()







