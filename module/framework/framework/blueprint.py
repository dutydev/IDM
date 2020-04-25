from module.objects.events import Event
from vkbottle.api import Api


class Blueprint:
    def __init__(self, name: str = None, description: str = None):
        self.api: Api = None
        self.on: Event = Event()
        self._name = name or "Unknown"
        self._description = description or "Unknown"
