import os
from datetime import datetime, timezone, timedelta


_DEBUG: bool = (os.environ.get('FLASK_ENV') == 'development')
_LOG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'duty.log'
)


class NamedWriter:
    def __init__(self, name):
        self.name = name

    def __call__(self, text):
        return self.info(text)

    def _write(self, text, level):
        date = datetime.now(timezone(timedelta(hours=3))).strftime(
            '%Y-%m-%d %H-%M-%S'
        )
        line = f"{date} | {level} ({self.name}) {text}"
        with open(_LOG_PATH, 'a', encoding='utf-8') as log:
            log.write(line + '\n')
        if _DEBUG:
            print(line)

    def trace(self, text):
        if not _DEBUG:
            return
        self._write(text, 'TRACE')

    def debug(self, text):
        if not _DEBUG:
            return
        self._write(text, 'DEBUG')

    def info(self, text):
        self._write(text, 'INFO')
        
    def warning(self, text):
        self._write(text, 'WARNING')

    def error(self, text):
        self._write(text, 'ERROR')

    def critical(self, text):
        self._write(text, 'CRITICAL')


def get_writer(name: str):
    return NamedWriter(name)


with open(_LOG_PATH + '.backup', 'w', encoding='utf-8') as backup:
    try:
        backup.write(open(_LOG_PATH, 'r', encoding='utf-8').read())
    except Exception:
        pass

open(_LOG_PATH, 'w').close()
