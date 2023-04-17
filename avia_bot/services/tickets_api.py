import requests

from avia_bot.config import HEADERS
from avia_bot.handlers.exceptions import CriticalExeption, NotCriticalExeption


def get_url(api, *args):
    """Шаблон URL для запроса к Aviasales API"""
    url = api.format(url_params=args)
    return url


def requests_handler(url):
    """Шаблон URL для запроса к Aviasales API"""
    with requests.Session() as check_source:
        request_to_api = check_source.get(url, params=None, headers=HEADERS, timeout=5.0)
        return request_to_api


def check_request_to_api(api, url_params):
    """Запрос к Aviasales API доступа данным по билетам"""
    url = get_url(api, *url_params)
    try:
        api_response = requests_handler(url)
    except requests.exceptions.Timeout:
        raise NotCriticalExeption
    except requests.exceptions.RequestException:
        raise CriticalExeption
    else:
        return api_response
