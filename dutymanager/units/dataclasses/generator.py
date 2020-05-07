from vkbottle.api.api.api import AbstractTokenGenerator
from dutymanager.files.dicts import default_data
from random import choice
from typing import List


class CustomTokenGenerator(AbstractTokenGenerator):
    def __init__(
        self,
        access_tokens: List[str],
        vk_me_token: str = None,
        online_token: str = None,
        friends_token: str = None,
    ):
        self.vk_me_token = vk_me_token
        self.access_tokens = access_tokens
        self.online_token = online_token
        self.friends_token = friends_token

    async def get_token(self, method: str, params: dict) -> str:
        if method in ("messages.setActivity", "messages.send"):
            return self.vk_me_token or choice(self.access_tokens)

        if method == "account.setOnline":
            return self.online_token

        if method.startswith("friends"):
            return self.friends_token
        return choice(self.access_tokens)


generator = CustomTokenGenerator(
    vk_me_token=default_data["me_token"],
    access_tokens=default_data["access_token"],
    friends_token=default_data["friends_token"],
    online_token=default_data["online_token"]
)