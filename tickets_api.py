import requests

from config import HEADERS
from exceptions import CriticalExeption, NotCriticalExeption
from template_messages import CRITICAL_WARNING_MESSAGE, NON_CRITICAL_WARNING_MESSAGE


def get_url(api, *args):
    """Шаблон URL для запроса к Aviasales API"""
    url = api.format(url_params=args)
    return url


def requests_handler(url):
    """Шаблон URL для запроса к Aviasales API"""
    with requests.Session() as check_source:
        try:
            request_to_api = check_source.get(
                url, params=None, headers=HEADERS, timeout=2.0
            )
            request_to_api.raise_for_status()
        except requests.exceptions.HTTPError:
            return "not_critical_error"
        except requests.exceptions.Timeout:
            return "not_critical_error"
        except requests.exceptions.RequestException:
            return "critical_error"
        else:
            return request_to_api


def check_request_to_api(api, url_params):
    """Запрос к Aviasales API доступа данным по билетам"""
    url = get_url(api, *url_params)
    api_response = requests_handler(url)
    if api_response == "critical_error":
        raise CriticalExeption(CRITICAL_WARNING_MESSAGE)
    if api_response == "not_critical_error":
        raise NotCriticalExeption(NON_CRITICAL_WARNING_MESSAGE)
    else:
        return api_response
