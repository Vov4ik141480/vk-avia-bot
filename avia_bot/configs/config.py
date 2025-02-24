import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "accept": "*/*",
}

VK_AVIA_BOT_GROUP_ID = os.getenv("VK_AVIA_BOT_GROUP_ID", "")

VK_BOT_TOKEN = os.getenv("VK_BOT_TOKEN", "")

AVIASALES_API_TOKEN = os.getenv("AVIASALES_API_TOKEN")

ALLOWED_PERIOD_FORMAT = ("на дату", "за месяц")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SQLITE_DB_FILE = BASE_DIR / "db.sqlite3"

API_USERS_GET_URL = "https://api.vk.com/method/users.get?user_ids={}&fields=city,contacts,country&access_token={}&v=5.131"

# URL для API автокомплита для стран, городов и аэропортов (IATA)
city_autocomplite_api_url = (
    "https://autocomplete.travelpayouts.com/places2?term={}&locale=ru&types[]=city"
)

# URL для API самых дешевых авиабилетов на определённые даты
aviasales_data_api_url = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={url_params[0]}&destination={url_params[1]}&currency=rub&departure_at={url_params[2]}&sorting=price&direct=false&limit=10&token={url_params[3]}"

# URL для API временных зон аэропортов
airports_timezone_api_url = (
    "https://api.travelpayouts.com/data/ru/airports.json?_gl=1*o4udno*_ga*MjkzMzM3NzM2LjE3NDAzMDU0NDU.*_ga_1WLL0NEBEH*MTc0MDMwNTQ0NS4xLjEuMTc0MDMwNzc4Ny4xNC4wLjA."
)
