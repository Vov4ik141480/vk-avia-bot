# coding: utf - 8
"""Обработчик данных от пользователя на правильность вводимой информации"""
import asyncio
import logging.config
import traceback

from attr import attrs, attrib

import city_names_api
import date_format_checker
import selection_confirmation
import exceptions
from vk_utils import period_keyboard, prove_keyboard
from bot_utils import BotSendMethod
from template_messages import message_for_period, message_for_depart, message_for_arrive, \
     CRITICAL_WARNING_MESSAGE, NON_CRITICAL_WARNING_MESSAGE
from conn_checker import get_connection_status
from config import ALLOWED_PERIOD_FORMAT
from log import log_config


logging.config.dictConfig(log_config)
logger = logging.getLogger("main")

@attrs
class Objects:
    bot = BotSendMethod()
    users_db = attrib()
    user_data_queue = attrib()
    complite_user_data_queue = attrib()

@attrs
class Period(Objects):
    def request_period(self, user_id, request_message):
        """Отправляет запрос юзеру выбрать период поиска"""
        keyboard = period_keyboard.get_keyboard()
        self.bot.send_message(user_id, request_message, keyboard)

    def check_period(self, user_message):
        """Проверяет правильность выбора периода из закрытого перечня"""
        if not user_message in ALLOWED_PERIOD_FORMAT:
            raise exceptions.WrongDataException

    def set_period(self, user_id, user_message):
        """Записывает в БД период"""
        self.users_db[user_id]["period"] = user_message

@attrs
class City(Objects):
    def request_city(self, user_id, request_message):
        """Отправляет запрос юзеру ввести название города отправления
        или прибытия, в зависимости от его статуса.
        """
        self.bot.send_message(user_id, request_message, None)

    def check_city(self, user_message):
        """Возвращает ответ от api проверки названия города"""
        city_name, airport_code = city_names_api.check_on_valid_city_name(
            user_message
        )
        return city_name, airport_code

    def set_city(self, user_id, key_word, city_name, airport_code):
        """Записывает в БД название города и код аэропорта"""
        flight_point_data = key_word
        self.users_db[user_id][flight_point_data] = [city_name, airport_code]

@attrs
class Date(Objects):
    def request_date(self, user_id):
        """Отправляет запрос юзеру ввести дату или месяц отправления,
        в зависимости от заданного юзером пириода поиска.
        """
        period = self.users_db[user_id]["period"]
        if period == "на дату":
            request_message = "Введите дату вылета в формате:\r\ndd-mm-yyyy"
        else:
            request_message = "Введите месяц в формате: mm-yyyy"
        self.bot.send_message(user_id, request_message, None)

    def check_date(self, user_id, message):
        """Возвращает актуальные дату или месяц вылета"""
        period = self.users_db[user_id]["period"]
        if period == "на дату":
            depart_date = date_format_checker.get_date(message)
        else:
            depart_date = date_format_checker.get_month(message)
        return depart_date

    def set_date(self, user_id, depart_date):
        """Записывает в БД дату или месяц отправления"""
        self.users_db[user_id]["date"] = depart_date


@attrs
class UserData(Period, City, Date):
    def switch_user_status(self, user_id, new_status):
        """Переопределяет статус юзера"""
        self.users_db[user_id]["status"] = new_status

    def send_proof(self, user_id, user_data):
        """Показывает юзеру консолидированные данные и спрашивает
        начинать поиск билетов или начать новый поиск.
        """
        depart_city = user_data["depart_data"]
        arrive_city = user_data["arrive_data"]
        departure_date = user_data["date"]
        collected_data = selection_confirmation.get_check_message(
            depart_city, arrive_city, departure_date
        )
        keyboard = prove_keyboard.get_keyboard()
        self.bot.send_message(user_id, collected_data, keyboard)

    def start_searching(self, user_id, user_message):
        """Отправляет приветственное сообщение новому юзеру,
        инициализирует новый поиск, отправляет info о боте,
        отправляет подсказку.
        """
        if user_message == "start":
            self.bot.send_welcome(user_id)
        elif user_message == "начать поиск":
            self.request_period(user_id, message_for_period)
            self.switch_user_status(user_id, "check_period")
        elif user_message == "help":
            self.bot.send_help(user_id)
        else:
            self.bot.send_hint(user_id)

    def get_period(self, user_id, user_message):
        """Проверяет правильно ли юзер ввел доступный период поиска.
        Если да, то записывает период в бд, переключает статус юзера
        и просит ввести название города отправления. Если название
        периода не соответствует формату, запрашивает пвторно.
        """
        try:
            self.check_period(user_message)
        except:
            warning_message = "Неверный период!"
            self.bot.send_warning(user_id, warning_message)
            self.request_period(user_id, message_for_period)
        else:
            self.set_period(user_id, user_message)
            self.switch_user_status(user_id, "check_depart_city")
            self.request_city(user_id, message_for_depart)

    def get_city_name(self, user_id, user_message, key_word, request_message, status):
        """Проверяет полученное от юзера название города отправления в API.
        Если название найдено, то получет название города и международный
        код аэропорта, записывает их в бд, переключает статус юзера и
        просит ввести название города прибытия. Если название не найдено
        предупреждает и запрашивает повторно.
        """
        try:
            city_name, airport_code = self.check_city(
                user_message
            )
        except exceptions.NotCriticalExeption:
            self.bot.send_warning(user_id, NON_CRITICAL_WARNING_MESSAGE)
            logger.info(traceback.format_exc(limit=2))
            self.request_city(user_id, request_message)
        except exceptions.CriticalExeption:
            self.bot.send_warning(user_id, CRITICAL_WARNING_MESSAGE)
            logger.error(traceback.format_exc(limit=2))
            raise 
        except exceptions.NotFoundException:
            warning_message = "Город с таким названием не найден!"
            self.bot.send_warning(user_id, warning_message)
            self.request_city(user_id, request_message)
        else:
            self.set_city(user_id, key_word, city_name, airport_code)
            self.switch_user_status(user_id, status)

    def get_depart_date(self, user_id, user_message):
        """Проверяет полученную от юзера дату/месяц на актуальность и
        соответствие заданному формату. Если данные соответствуют
        записывает их в бд и инициирует запрос на поиск билетов,
        если данные не верны - предупреждает и запрашивает период повторно.
        """
        try:
            depart_date = self.check_date(user_id, user_message)
        except exceptions.WrongDateFormat:
            warning_message = "Ошибка в дате или неверный фоормат! Введите повторно."
            self.bot.send_warning(user_id, warning_message)
            self.request_date(user_id)
        except exceptions.DateNotCorrect:
            warning_message = "Дата должна соответствовать текущему или будущему периоду! Введите повторно."
            self.bot.send_warning(user_id, warning_message)
            self.request_date(user_id)
        else:
            self.set_date(user_id, depart_date)
            self.switch_user_status(user_id, "ready_for_proof")
            self.send_proof(user_id, self.users_db[user_id])

    def get_proof(self, user_id, user_message):
        """Получает от юзера ответ. Если ответ положительный ставит данные
        по выбранному направлению в очередь верифицированных данных, либо
        инициирует новый поиск.
        """
        if user_message == "да":
            self.switch_user_status(user_id, "complit")
            complit_data = self.users_db.pop(user_id)
            formatted_data = selection_confirmation.verified_user_data(
                user_id, complit_data
            )
            self.complite_user_data_queue.put_nowait(formatted_data)
        else:
            self.request_period(user_id, message_for_period)
            self.switch_user_status(user_id, "check_period")


    async def data_handler(self):
        """Запоминает статус для каждого юзера, распределяет данные для
        проверки по соответствующим текущему статусу методам, записывает
        проверенные данные в БД, получает от пользователя подтверждение
        и отправляет верифицированные данные из БД в очередь.
        """
        while await get_connection_status():
            try:
                while not self.user_data_queue.empty():
                    user_data = await self.user_data_queue.get()
                    user_id = user_data.user_id
                    user_message = user_data.text
                    self.user_data_queue.task_done()

                    if user_id in self.users_db:
                        user_status = self.users_db[user_id]["status"]

                        if user_message == "начать поиск" or user_message == "start":
                            self.start_searching(user_id, user_message)
                        elif user_status == "check_period":
                            self.get_period(user_id, user_message)
                        elif user_status == "check_depart_city":
                            key_word = "depart_data"
                            next_status = "check_arrive_city"
                            self.get_city_name(user_id, user_message, key_word, message_for_depart, next_status)
                            self.request_city(user_id, message_for_arrive)
                        elif user_status == "check_arrive_city":
                            key_word = "arrive_data"
                            next_status = "check_date"
                            self.get_city_name(user_id, user_message, key_word, message_for_arrive, next_status)
                            self.request_date(user_id)
                        elif user_status == "check_date":
                            self.get_depart_date(user_id, user_message)
                        elif user_status == "ready_for_proof":
                            self.get_proof(user_id, user_message)
                        else:
                            self.start_searching(user_id, user_message)

                    else:
                        self.start_searching(user_id, user_message)
            except Exception:
                continue


async def main(users_db, user_request_data, complite_user_data):
    user_data = UserData(
        users_db, user_request_data, complite_user_data
    )
    await asyncio.gather(
        asyncio.create_task(user_data.data_handler()),
        asyncio.create_task(user_data.data_handler()),
        return_exceptions=True,
    )


def start(users_db, user_request_data, complite_user_data):
    asyncio.run(
        main(users_db, user_request_data, complite_user_data)
    )
