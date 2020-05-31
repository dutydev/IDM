from vkbottle.user import User as Bot

DEFAULT_WAIT: int = 25


class User(Bot):

    long_poll_server: dict
    wait: int
    version: int = None

    @property
    def stopped(self) -> bool:
        return self._stop

    @stopped.setter
    def stopped(self, value: bool):
        self._stop = value