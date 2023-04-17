# coding: utf-8
import time
from datetime import datetime

from avia_bot.handlers.exceptions import WrongDateFormat, DateNotCorrect


def get_date(user_date):
    """Проверяет чтобы дата была не ранее чем текущая и возвращает
    дату отправления
    """
    time_now = datetime.now()
    date_now = time_now.strftime("%d-%m-%Y")
    current_date = time.strptime(date_now, "%d-%m-%Y")
    try:
        valid_flight_date = time.strptime(user_date, "%d-%m-%Y")
    except ValueError:
        raise WrongDateFormat
    else:
        if valid_flight_date >= current_date:
            formatted_date = time.strftime("%d-%m-%Y", valid_flight_date)
            return formatted_date
        else:
            raise DateNotCorrect


def get_month(user_date):
    """Проверяет чтобы месяц был не ранее чем текущий и возвращает
    месяц отправления
    """
    time_now = datetime.now()
    date_now = time_now.strftime("%m-%Y")
    current_month = time.strptime(date_now, "%m-%Y")
    try:
        valid_flight_month = time.strptime(user_date, "%m-%Y")
    except ValueError:
        raise WrongDateFormat 
    else:
        if valid_flight_month >= current_month:
            formatted_month = time.strftime("%m-%Y", valid_flight_month)
            return formatted_month
        else:
            raise DateNotCorrect
