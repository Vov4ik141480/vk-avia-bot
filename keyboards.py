
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def make_keyboards():
    keyboard = VkKeyboard(one_time=False, inline=False)
    keyboard.add_button(label="начать поиск", color=VkKeyboardColor.PRIMARY, payload={"text": "search"})
    return keyboard


def represent_search_type():
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_button(label="на дату", color=VkKeyboardColor.PRIMARY, payload={"text": "for_date"})
    keyboard.add_button(label="за месяц", color=VkKeyboardColor.PRIMARY, payload={"text": "for_month"})
    return keyboard


def keyboard_desision():
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_button(label="да", color=VkKeyboardColor.POSITIVE, payload={"text": "yes"})
    keyboard.add_button(label="новый поиск", color=VkKeyboardColor.NEGATIVE, payload={"text": "change"})
    return keyboard


def keyboard_change_dissision():
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_button(label="Город отправления", color=VkKeyboardColor.PRIMARY, payload={"text": "dep_city"})
    keyboard.add_line()
    keyboard.add_button(label="Город прибытия", color=VkKeyboardColor.PRIMARY, payload={"text": "arrive_city"})
    keyboard.add_line()
    keyboard.add_button(label="Дата вылета", color=VkKeyboardColor.PRIMARY, payload={"text": "date"})
    return keyboard


def keyboard_get_link(link=None):
    keyboard = VkKeyboard(one_time=False, inline=True)
    keyboard.add_openlink_button(label="купить на aviasales.com", link=link, payload={"type": "open_link"})
    return keyboard
