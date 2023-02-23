# coding: 'utf' - 8
"""Сервер Vk бота"""
import asyncio
from collections import defaultdict, deque

import get_user_data
import get_ticket_data
import send_result 
from worker import Worker
from vk_longpoll import VkServer


class Bot:
    def __init__(self):
        self.data_queue = asyncio.Queue()
        self.messages_queue = asyncio.Queue()
        self.db = defaultdict(dict)
        self.complite_users_data_queue = asyncio.Queue()
        self.events_queue = deque()
        self.tickets_queue = deque()
        self.vk_server = VkServer(self.events_queue)
        self.worker = Worker(self.events_queue, self.messages_queue)

    def start(self):
        """Запускает компаненты бота (корутины) в бесконечном цикле"""
        loop = asyncio.get_event_loop()
        poller = loop.create_task(self.vk_server.get_event())
        worker = loop.create_task(self.worker._worker())
        loop.run_in_executor(
            None, 
            get_user_data.start, 
            self.db, 
            self.messages_queue,
            self.complite_users_data_queue
            )
        loop.run_in_executor(
            None,
            get_ticket_data.start,
            self.complite_users_data_queue,
            self.tickets_queue
            )
        loop.run_in_executor(None, send_result.start, self.tickets_queue)                    
        tasks = asyncio.gather(poller, worker)
        loop.run_until_complete(tasks)
        
        """В случае получения сигнала остановки цикла собирает не 
        завершенные задачи, отменяет их, затем снова запускает цикл, 
        пока эти задачи не будут выполнены
        """
        pending = asyncio.all_tasks(loop=loop) 
        for task in pending:
            task.cancel()
        group = asyncio.gather(*pending, return_exceptions=True) 
        loop.run_until_complete(group)
        loop.close()


def main():
    """Запуск Vk бота"""
    bot = Bot()
    try:
        bot.start()
    except Exception as exc:
        print(exc.args[0])


if __name__ == "__main__":
    main()
