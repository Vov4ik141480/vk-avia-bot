import requests

from avia_bot.config import API_USERS_GET_URL, VK_BOT_TOKEN, HEADERS
from avia_bot.handlers.exceptions import CriticalExeption, NotCriticalExeption


def get_user(uid):
    with requests.Session() as session:
        try:
            api_response = session.get(
                API_USERS_GET_URL.format(uid, VK_BOT_TOKEN),
                headers=HEADERS,
                params=None,
                timeout=5.0,
            )
            api_response.raise_for_status()
        except requests.exceptions.HTTPError:
            raise NotCriticalExeption
        except requests.exceptions.Timeout:
            raise NotCriticalExeption
        except requests.exceptions.RequestException:
            raise CriticalExeption
        else:
            api_response = api_response.json()
            return api_response["response"][0]
