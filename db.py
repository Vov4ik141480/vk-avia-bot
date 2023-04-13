import sqlite3
import logging.config
import traceback

import config
from log import log_config


logging.config.dictConfig(log_config)
logger = logging.getLogger("main")

def get_db():
    con = sqlite3.Connection(config.SQLITE_DB_FILE)
    return con


def execute(sql, params):
    try:
        db = get_db()
        with db:
            db.execute(sql, params)
    except sqlite3.Error:
        logger.error(traceback.format_exc(limit=2))
    finally:
        close_db()


def close_db():
    db = get_db()
    db.close()
