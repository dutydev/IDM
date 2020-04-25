from vkbottle.api.api.token import AbstractTokenGenerator
from dutymanager.core.config import default_data
import typing
import random


class CustomTokenGenerator(AbstractTokenGenerator):
    def __init__(self, vk_me_tokens: typing.List[str], tokens: typing.List[str]):
        self.vk_me_tokens = vk_me_tokens
        self.tokens = tokens

    async def get_token(self, method: str, params: dict) -> str:
        if method in ["messages.setActivity", "messages.send"]:
            return random.choice(self.vk_me_tokens)
        return random.choice(self.tokens)


generator = CustomTokenGenerator(
    vk_me_tokens=[default_data["me_token"]],
    tokens=[default_data["access_token"]]
)