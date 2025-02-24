from datetime import datetime

from avia_bot.handlers.db_handler import execute_add


def insert_ticket(user_request):
    query = "INSERT INTO ticket (departure_city, destination_city, depart_date, search_date, ticket_uid) \
            VALUES (:departure_city, :destination_city, :depart_date, :search_date, :ticket_uid)"
    ticket_data = {
            "departure_city": user_request["departure_point"],
            "destination_city": user_request["arrival_point"],
            "depart_date": user_request["depart_at"],
            "search_date": datetime.now().strftime('%Y-%m-%d'),
            "ticket_uid": user_request["user_id"]
    }
    execute_add(query, ticket_data)
