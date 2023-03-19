# coding: utf-8
import requests

from config import city_autocomplite_api_url, HEADERS
from exceptions import CriticalExeption, NotCriticalExeption, NotFoundException


def requests_handler(url):
    """Делает запрос Aviasales API автокомплита городов и возвращает
    полученные данные
    """
    with requests.Session() as check_source:
        try:
            response = check_source.get(url, headers=HEADERS, params=None, timeout=1.0)
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            return ("not_critical_error", exc)
        except requests.exceptions.Timeout as exc:
            return ("not_critical_error", exc)
        except requests.exceptions.RequestException as exc:
            return ("critical_error", exc)
        else:
            return response


def check_on_valid_city_name(city_name):
    """Инициирует запрос к API автокомплита городов, обрабатывает ответ
    и возвращает данные (название города и код аэропорта)
    """
    url = city_autocomplite_api_url.format(city_name)
    api_response = requests_handler(url)
    if api_response[0] == "critical_error":
        raise CriticalExeption(api_response[1])
    if api_response[0] == "not_critical_error":
        raise NotCriticalExeption(api_response[1])
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
