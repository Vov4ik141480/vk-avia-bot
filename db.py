import sqlite3

import config


def get_db():
    con = sqlite3.Connection(config.SQLITE_DB_FILE)
    return con


def execute(sql, params):
    db = get_db()
    cur = db.cursor()
    args = (sql, params)
    cur.execute(*args)
    db.commit()


def close_db():
    db = get_db()
    db.close()
