from db import execute


def insert_ticket(user_request):
    execute(
        "INSERT INTO ticket (departure_city, destination_city, depart_date, user_id) VALUES \
            (:departure_city, :destination_city, :depart_date, :user_id)",
        {
            "departure_city": user_request["departure_point"],
            "destination_city": user_request["arrival_point"],
            "depart_date": user_request["depart_at"],
            "user_id": user_request["user_id"]
        },
    )
