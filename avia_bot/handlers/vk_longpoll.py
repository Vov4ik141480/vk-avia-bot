"""VK longpoll сервер"""
import asyncio

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from avia_bot.config import VK_BOT_TOKEN, VK_AVIA_BOT_GROUP_ID


class VkServer:
    def __init__(self, events_queue):
        self.token = VK_BOT_TOKEN
        self.vk_session = vk_api.VkApi(token=self.token)
        self.longpoll = VkBotLongPoll(self.vk_session, VK_AVIA_BOT_GROUP_ID)
        self.vk = self.vk_session.get_api()
        self.events_queue = events_queue

    async def get_event(self):
        """Слушает vk сервер, ловит событие от юзера и ставит данные 
        в очередь событий.
        """
        while True:
            for event in self.longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
                    self.events_queue.appendleft(event.obj.message)
                    await asyncio.sleep(0.1)
