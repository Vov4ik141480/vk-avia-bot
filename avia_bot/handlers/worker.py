# coding: utf - 8
"""Компонент Vk бота - Worker"""
import asyncio
from collections import namedtuple


class Worker:
    def __init__(self, events_queue, messages_queue):
        self.events_queue = events_queue
        self.messages_queue = messages_queue

    async def _worker(self):
        """Берет данные из очереди событий, извлекает данные
        и ставит в очередь сообщений.
        """
        while True:
            if self.events_queue:
                user_response = self.events_queue.pop()
                user_id = user_response["from_id"]
                text = user_response["text"].lower()
                Response = namedtuple("Response", ["user_id", "text"])
                await self.messages_queue.put(Response(user_id, text))
            else:
                await asyncio.sleep(0.1)
