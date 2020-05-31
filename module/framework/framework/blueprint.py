from vkbottle.framework.framework.handler.middleware import MiddlewareExecutor
from vkbottle.framework.framework.handler.user import UserHandler
from module.framework.error_handler import ErrorHandler
from module.objects.events import Event
from vkbottle.api import UserApi


class Blueprint:
    def __init__(self, name: str = None, description: str = None):
        # Main Workers
        self.api: UserApi = None
        self.on: UserHandler = UserHandler()
        self.middleware: MiddlewareExecutor = MiddlewareExecutor()
        self.event: Event = Event()

        # Sign assets
        self.user_id: int = None
        self._name = name or "Unknown"
        self._description = description or "Unknown"
        self.error_handler: ErrorHandler = ErrorHandler()

    def create(self, api_instance: UserApi, user_id: int):
        self.api = api_instance
        self.user_id = user_id