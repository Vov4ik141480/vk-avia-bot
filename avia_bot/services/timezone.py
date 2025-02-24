from avia_bot.handlers.db_handler import execute_get


def get_airport_timezone(airport_code):
    query = "SELECT time_zone FROM iata_time_zone WHERE iata_code = ? LIMIT 1"
    response = execute_get(query, (airport_code,))
    return response[0]
