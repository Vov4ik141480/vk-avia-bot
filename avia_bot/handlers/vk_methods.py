"""VK longpoll сервер"""
import vk_api
from vk_api.utils import get_random_id

from avia_bot.configs.config import VK_BOT_TOKEN


class VkMethods:
    def __init__(self):
        self.token = VK_BOT_TOKEN
        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()

    def send_message(self, user_id, text, keyboard):
        """Отправляет сообщение юзеру"""
        self.vk.messages.send(
            user_id = user_id,
            random_id=get_random_id(),
            peer_id=user_id,
            keyboard=keyboard,
            message=text
        )
