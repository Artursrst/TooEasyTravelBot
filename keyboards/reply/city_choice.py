from telebot.types import Message
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def city_markup() -> Message:
    destinations = InlineKeyboardMarkup()
    cities = [['Нью-Йорк', 'new_york'], ['Лос-Анджелес', 'los_angeles'],['Чикаго', 'chicago'], ['Хьюстон', 'houston'], ['Филадельфия', 'philadelphia'],
              ['Сан-Антонио', 'san_antonio'], ['Даллас', 'dallas'], ['Сан-Хосе', 'san_jose'], ['Сан-Франциско', 'san_francisco']]
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city[0],
                          callback_data=city[1]))
    return destinations

