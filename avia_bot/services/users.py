from avia_bot.services.user_data_api import get_user
from avia_bot.handlers.db_handler import execute_add


def insert_user(uid):
    try:
        user_data = get_user(uid)
    except Exception():
        return
    else:
        query = "INSERT OR IGNORE INTO user (user_id, first_name, last_name, mobile_phone) VALUES (?, ?, ?, ?)"
        personal_data = (
            user_data["id"],
            user_data["first_name"],
            user_data["last_name"],
            user_data.get("mobile_phone", None)
        )
        execute_add(query, personal_data)
