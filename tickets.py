from db import execute


def insert_ticket(user_request):
    execute(
        "INSERT INTO TABLE ticket (departure_city, destination_city, depart_date) VALUES (?, ?, ?)",
        (
            user_request["departure_city"],
            user_request["destination_city"],
            user_request["depart_date"],
        ),
    )
