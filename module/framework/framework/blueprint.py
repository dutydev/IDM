from vkbottle.framework.framework.handler.user import Handler
from module.objects.events import Event
from vkbottle.api import UserApi


class Blueprint:
    def __init__(self, name: str = None, description: str = None):
        self.api: UserApi = None
        self.on: Handler = Handler()
        self.event: Event = Event()
        self._name = name or "Unknown"
        self._description = description or "Unknown"

    def create(self, api_instance: UserApi):
        self.api = api_instance
