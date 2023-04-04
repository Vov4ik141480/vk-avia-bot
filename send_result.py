import asyncio
from datetime import datetime

from template_messages import ticket_data
from keyboards import keyboard_get_link
from bot_utils import BotSendMethod
from conn_checker import get_connection_status


async def get_data(tickets_queue):
    """Отправляет пользователю найденные билеты или оповещает, что по направлению
    билеты не найдены"""
    while await get_connection_status():    
        if tickets_queue:
            ticket_data_set = tickets_queue.pop()
            await asyncio.to_thread(send_result, ticket_data_set)


def send_result(ticket_data_set):
    user_id = ticket_data_set[0]
    flight_data = ticket_data_set[1]
    if isinstance(flight_data, str):
        BotSendMethod().send_message(user_id, flight_data, None)
    else:
        for ticket in flight_data:
            ticket_message = ticket_data.format(
                ticket.departure_city,
                ticket.arrival_city,
                ticket.origin_airport,
                ticket.depart_datetime,
                ticket.destination_airport,
                ticket.arrive_datetime,
                ticket.price,
                ticket.transfers,
            )
            keyboard = keyboard_get_link(ticket.ticket_link).get_keyboard()
            BotSendMethod().send_message(user_id, ticket_message, keyboard)


async def main(tickets_queue):
    await asyncio.gather(
        asyncio.create_task(get_data(tickets_queue)),
        asyncio.create_task(get_data(tickets_queue)),
    )


def start(tickets_queue):
    asyncio.run(main(tickets_queue))
