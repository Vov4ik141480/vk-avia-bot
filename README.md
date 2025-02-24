# [AVIA-BOT](https://vk.com/public209580430)

This chatbot in the social network Vkontakte was made for people who are looking for a chip flight tickets.
The chatbot gets ticket insights and flight price from the Aviasales Data API.

## Bot commands

- 'start' - приветственное сообщение
- 'help' - справка
- 'начать поиск' - новый поиск

## Instalation
> - create vk bot to communicate with users throw the community;
> - create an account on the [Travel Partnership Platform](https://support.travelpayouts.com/hc/en-us/articles/203955593-Getting-started), choose Aviasales as the project and fill out the information;
> - Rename the .env.example file into .env and modify it according to the ids and tokens recieved.

## Database configuration
From project root folder run next scripts:
``` shell
# Create the required database tables.

sqlite3 db.sqlite3 < avia_bot/configs/db.sql
```

``` shell
# Enable Foreign key constraint.

sqlite3 db.sqlite3
PRAGMA foreign_keys = ON;
.exit
```

``` shell
# Get airports timezones data from API and fill with them table.

python3 airports_timezone_fill_db.py
```

### Requirements
> - Python 3.9
> - PIP (Python Dependency Manager)

### Dependency
> - Install relevant dependencies with: pip install -r requirements.txt

## Roadmap
> добавить выбор языка (EN/RU)
