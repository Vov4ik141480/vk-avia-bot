# coding: utf-8
"""Сервис по получению авиабилетов"""
import asyncio
from datetime import datetime, timedelta
from typing import NamedTuple

import arrow

import tickets_api
from config import (
    aviasales_data_api_url,
    airports_timezone_api_url,
    AVIASALES_API_TOKEN,
)
from exceptions import CriticalExeption, NotCriticalExeption, DateNotCorrect
from template_messages import no_tickets_find
from exceptions import CriticalExeption, NotCriticalExeption
from bot_utils import BotSendMethod
from conn_checker import get_connection_status


class Message(NamedTuple):
    """Стркутура распаршенного сообщения о найденном билете"""
    departure_city: str
    arrival_city: str
    origin_airport: str
    destination_airport: str
    price: str
    transfers: str
    depart_datetime: datetime
    arrive_datetime: datetime
    ticket_link: str


class FlightData:
    def __init__(self, user_request_data, tickets_queue):
        self.user_data = user_request_data
        self.user_id = self.user_data["user_id"]
        self.departure_city_name = self.user_data["departure_point"]
        self.arrival_city_name = self.user_data["arrival_point"]
        self.depart_city_code = self.user_data["departure_point_code"]
        self.arrive_citi_code = self.user_data["arrival_point_code"]
        self.departure_time = self.user_data["depart_at"]
        self.api_token = AVIASALES_API_TOKEN
        self.tickets_portfolio = []
        self.bot_ = BotSendMethod()
        self.tickets_queue = tickets_queue

    def make_request_to_api_for_date(self):
        """Возвращает список найденных билетов на текущую или
        будущую дату
        """
        api = aviasales_data_api_url
        url_params = [
            self.depart_city_code,
            self.arrive_citi_code,
            self.departure_time,
            self.api_token,
        ]
        while True:
            try:
                request_to_api_for_date = tickets_api.check_request_to_api(
                    api, url_params
                )
            except NotCriticalExeption as exc:
                self.bot_.send_warning(self.user_id, exc.args[0])
                continue
            except CriticalExeption as exc:
                raise exc
            else:
                if request_to_api_for_date.json()["data"]:
                    try:
                        departure_date = request_to_api_for_date.json()["data"][0][
                            "departure_at"
                        ]
                        self.check_new_date(departure_date)
                    except DateNotCorrect as exc:
                        self.bot_.send_warning(self.user_id, exc.args[0])
                        self.departure_time = exc.args[1]
                        continue
                    else:
                        return self.api_response_handle(request_to_api_for_date)
                else:
                    return no_tickets_find

    def make_requests_to_api_for_month(self):
        """Возвращает список найденных билетов на ближайшие даты месяца"""
        api = aviasales_data_api_url
        url_params = [
            self.depart_city_code,
            self.arrive_citi_code,
            self.departure_time,
            self.api_token,
        ]
        self.departure_time = self.departure_time[0:7]
        while True:
            try:
                request_to_api_for_month = tickets_api.check_request_to_api(
                    api, url_params
                )
            except NotCriticalExeption as exc:
                self.bot_.send_warning(self.user_id, exc.args[0])
                continue
            except CriticalExeption as exc:
                raise exc
            else:
                if request_to_api_for_month.json()["data"]:
                    return self.api_response_handle(request_to_api_for_month)
                else:
                    return no_tickets_find

    def get_depart_datetime(self, departure_at):
        """Возвращает дату/время вылета в формате ДД-ММ-ГГГГ ЧЧ:ММ"""
        standart_depart_dt = arrow.get(departure_at)
        depart_datetime = standart_depart_dt.format("DD-MM-YYYY HH:mm")
        return depart_datetime

    def get_arrive_datetime(self, departure_at, timezone, flight_duration):
        """Возвращает дату/время прилета в формате ДД-ММ-ГГГГ ЧЧ:ММ"""
        standart_depart_dt = arrow.get(departure_at)
        depart_tz_to_arrive_tz = standart_depart_dt.to(timezone)
        arrive_datetime = depart_tz_to_arrive_tz + timedelta(minutes=flight_duration)
        return arrive_datetime.format("DD-MM-YYYY HH:mm")

    def check_new_date(self, departure_date):
        """Если билетов до конца дня нет, меняет дату поиска (Т+1)
        и инициирует поиск билетов на новую дату"""
        if arrow.now() < (arrow.get(departure_date) + timedelta(hours=1)):
            return True
        else:
            next_date = arrow.now() + timedelta(days=1)
            departure_time = next_date.date()
            raise DateNotCorrect(
                "На сегодня билетов уже нет. Ищу на затра ...",
                departure_time.strftime("%Y-%m-%d"),
            )

    def get_transfer_data(self, transfers):
        """Возвращает данные о количестве пересадок"""
        transfers_value = transfers
        if transfers_value == 0:
            return "Без пересадок"
        elif transfers_value == 1:
            return "1 пересадка"
        elif 2 <= transfers_value < 5:
            return f"{transfers_value} пересадки"
        else:
            return f"{transfers_value} пересадок"

    def get_timezones(self, airport_code):
        """Возвращает временную зону аэропорта назначения"""
        api = airports_timezone_api_url
        url_param = [airport_code.lower()]
        while True:
            try:
                request_to_api_for_timezone = tickets_api.check_request_to_api(
                    api, url_param
                )
            except NotCriticalExeption as exc:
                self.bot_.send_warning(self.user_id, exc.args[0])
                continue
            except CriticalExeption as exc:
                raise exc
            else:
                airport_timezone = request_to_api_for_timezone.json()["timezone"]
                return airport_timezone

    def api_response_handle(self, request_to_api):
        """Обрабатывет результат запроса к API и возвращает список из
        данных по билетам
        """
        current_destination_airport = request_to_api.json()["data"][0][
            "destination_airport"
        ]
        arrive_timezone = self.get_timezones(current_destination_airport)

        for ticket_data in request_to_api.json()["data"]:
            flight_duration = ticket_data["duration"]
            departure_date = ticket_data["departure_at"]
            destination_airport = ticket_data["destination_airport"]
            if destination_airport != current_destination_airport:
                arrive_timezone = self.get_timezones(destination_airport)
                current_destination_airport = destination_airport
            depart_datetime = self.get_depart_datetime(departure_date)
            arrive_datetime = self.get_arrive_datetime(
                departure_date, arrive_timezone, flight_duration
            )
            transfer_data = self.get_transfer_data(ticket_data["transfers"])

            ticket = Message(
                departure_city=self.departure_city_name,
                arrival_city=self.arrival_city_name,
                origin_airport=ticket_data["origin_airport"],
                destination_airport=ticket_data["destination_airport"],
                price=ticket_data["price"],
                depart_datetime=depart_datetime,
                arrive_datetime=arrive_datetime,
                transfers=transfer_data,
                ticket_link="https://www.aviasales.ru" + ticket_data["link"],
            )
            self.tickets_portfolio.append(ticket)
        return self.tickets_portfolio

    def get_ticket_data_from_api(self):
        """Делает запрос к API, полученные данные ставит в очередь билетов"""
        if self.user_data["period"] == "на дату":
            date_api_response = self.make_request_to_api_for_date()
            self.tickets_portfolio = []
            self.tickets_queue.appendleft([self.user_id, date_api_response])
        else:
            month_api_response = self.make_requests_to_api_for_month()
            self.tickets_portfolio = []
            self.tickets_queue.appendleft([self.user_id, month_api_response])


async def process_job(complite_user_data, tickets_queue):
    """Берет из очереди готовые данные, создает экземпляр класса FlightData
    и в отдельном потоке запускает запрос к API
    """
    while await get_connection_status():
        try:
            if not complite_user_data.empty():
                user_data = await complite_user_data.get()
                flight_data = FlightData(user_data, tickets_queue)
                complite_user_data.task_done()
                await asyncio.to_thread(flight_data.get_ticket_data_from_api)
        except Exception as exc:
            raise exc

async def main(complite_user_data, tickets_queue):
    await asyncio.gather(
        asyncio.create_task(process_job(complite_user_data, tickets_queue)),
        asyncio.create_task(process_job(complite_user_data, tickets_queue)),
    )


def start(complite_user_data, tickets_queue):
    asyncio.run(main(complite_user_data, tickets_queue))
