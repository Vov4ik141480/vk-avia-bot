from user_data_api import get_user
from db import execute


def insert_user(uid):
    try:
        user_data = get_user(uid)
    except Exception():
        return
    else:
        personal_data = (
            user_data["id"],
            user_data["first_name"],
            user_data["last_name"],
            user_data["mobile_phone"],
        )
        execute(
            "INSERT INTO TABLE user (uid, first_name, last_name, mobile_phone) VALUES (?, ?, ?, ?)",
            personal_data,
        )
