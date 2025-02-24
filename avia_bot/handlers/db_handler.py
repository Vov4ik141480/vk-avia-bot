import sqlite3
import logging.config
import traceback

import avia_bot.configs.config as config
from avia_bot.handlers.log import log_config


logging.config.dictConfig(log_config)
logger = logging.getLogger("main")

def get_conn():
    conn = sqlite3.Connection(config.SQLITE_DB_FILE)
    return conn


def execute_add(query, params):
    with get_conn() as connection:
        cursor = connection.cursor()

        try:
            with connection:
                cursor.execute(query, params)
                connection.commit()
        except sqlite3.Error:
            logger.error(traceback.format_exc(limit=2))  


def execute_get(query, params):
    with get_conn() as connection:
        cursor = connection.cursor()

        try:
            with connection:
                cursor.execute(query, params)
                return cursor.fetchone()
        except sqlite3.Error:
            logger.error(traceback.format_exc(limit=2))      


def close_db():
    conn = get_conn()
    conn.close()
