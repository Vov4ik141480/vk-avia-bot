# coding: utf-8
import requests

from config import city_autocomplite_api_url, HEADERS
from exceptions import CriticalExeption, NotCriticalExeption, NotFoundException
from template_messages import CRITICAL_WARNING_MESSAGE, NON_CRITICAL_WARNING_MESSAGE


def requests_handler(url):
    """Делает запрос Aviasales API автокомплита городов и возвращает
    полученные данные
    """
    with requests.Session() as check_source:
        try:
            response = check_source.get(url, headers=HEADERS, params=None, timeout=1.0)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return "not_critical_error"
        except requests.exceptions.Timeout:
            return "not_critical_error"
        except requests.exceptions.RequestException:
            return "critical_error"
        else:
            return response


def check_on_valid_city_name(city_name):
    """Инициирует запрос к API автокомплита городов, обрабатывает ответ
    и возвращает данные (название города и код аэропорта)
    """
    url = city_autocomplite_api_url.format(city_name)
    api_response = requests_handler(url)
    if api_response == "critical_error":
        raise CriticalExeption(CRITICAL_WARNING_MESSAGE)
    if api_response == "not_critical_error":
        raise NotCriticalExeption(NON_CRITICAL_WARNING_MESSAGE)
    else:
        city_name_matches = api_response.json()
        if city_name_matches:
            valid_city_name = [
                city_name_matches[0]["name"],
                city_name_matches[0]["code"],
            ]
            return valid_city_name
        else:
            raise NotFoundException
