import sqlite3

import config


def get_db():
    con = sqlite3.Connection(config.SQLITE_DB_FILE)
    return con
