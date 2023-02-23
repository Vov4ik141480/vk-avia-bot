from datetime import datetime

from template_messages import result_message


def get_check_message(depart_city, arrive_city, user_date):
    """Возвращает текст сообщения, составленного для 
    подтверждения юзером правильного набора данных.
    """
    return result_message.format(depart_city[0], arrive_city[0], user_date)


def verified_user_data(user_id, *args):
    """Возвращает подтвержденные юзером данные в формате для запроса к
    Aviasales API доступа данным по билетам
    """
    period = args[0]["period"]
    depart_city_name = args[0]["depart_data"][0]
    depart_city_code = args[0]["depart_data"][1]
    arrive_city_name = args[0]["arrive_data"][0]
    arrive_city_code = args[0]["arrive_data"][1]
    depart_date = args[0]["date"]
    if period == "на дату":
        utc_user_date = datetime.strptime(depart_date, "%d-%m-%Y")
        date = utc_user_date.strftime("%Y-%m-%d")
    else:
        utc_user_date = datetime.strptime(depart_date, "%m-%Y")
        date = utc_user_date.strftime("%Y-%m")
    return {
        "user_id": user_id,
        "period": period,
        "departure_point": depart_city_name,
        "arrival_point": arrive_city_name,
        "departure_point_code": depart_city_code,
        "arrival_point_code": arrive_city_code,
        "depart_at": date
    }
