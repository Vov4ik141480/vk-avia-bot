import requests
import logging.config
import traceback

from avia_bot.config import airports_timezone_api_url
from avia_bot.db import get_conn
from avia_bot.log import log_config


logging.config.dictConfig(log_config)
logger = logging.getLogger("main")


def get_airports_timezone():
    api_data = requests.get(airports_timezone_api_url)
    return api_data.json()


def insert_data():
    try:
        json_data = get_airports_timezone
        records = [(item["code"], item["time_zone"]) for item in json_data]
        conn = get_conn()
        with conn.cursor() as cursor:
            cursor.executemany(
                "INSERT INTO iata_time_zone (iata_code, time_zone) VALUES (?, ?)",
                records
            )
    except Exception():
        logger.error(traceback.format_exc(limit=2))


if __name__ == '__main__':
    insert_data()
