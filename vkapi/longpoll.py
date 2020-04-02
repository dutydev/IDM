import requests

from . import VkApi


class LongPoll(object):

    DEFAULT_WAIT: int = 25
    long_poll_server: dict

    def __init__(self, api: VkApi, group_id: int, wait: int = DEFAULT_WAIT):
        self.api = api
        self.group_id = group_id
        self.__wait = wait

    def get_server(self) -> dict:
        self.long_poll_server = self.api("groups.getLongPollServer", group_id=self.group_id)
        return self.long_poll_server

    def make_long_request(self, long_poll_server: dict) -> dict:
        """
        Make longPoll request to the VK Server
        :param long_poll_server:
        :return: VK LongPoll Event
        """
        url = "{}?act=a_check&key={}&ts={}&wait={}&rps_delay=0".format(
            long_poll_server["server"],
            long_poll_server["key"],
            long_poll_server["ts"],
            self.__wait,
        )
        return requests.post(url).json()

    def check(self):
        self.get_server()
        self.api.logger.info("Polling successfully started. Press Ctrl+C to stop it")

        event = self.make_long_request(self.long_poll_server)
        if isinstance(event, dict) and event.get("ts"):
            self.long_poll_server["ts"] = event["ts"]
            return event
        else:
            self.get_server()

    def listen(self):
        while True:
            yield self.check()
