# coding: utf-8
import requests

from avia_bot.configs.config import city_autocomplite_api_url, HEADERS
from avia_bot.handlers.exceptions import CriticalExeption, NotCriticalExeption, NotFoundException


def requests_handler(url):
    """Делает запрос Aviasales API автокомплита городов и возвращает
    полученные данные
    """
    with requests.Session() as check_source:
        response = check_source.get(url, headers=HEADERS, params=None, timeout=5.0)
        return response


def check_on_valid_city_name(city_name):
    """Инициирует запрос к API автокомплита городов, обрабатывает ответ
    и возвращает данные (название города и код аэропорта)
    """
    url = city_autocomplite_api_url.format(city_name)
    try:
        api_response = requests_handler(url)
        api_response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise NotCriticalExeption
    except requests.exceptions.Timeout:
        raise NotCriticalExeption
    except requests.exceptions.RequestException:
        raise CriticalExeption
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
