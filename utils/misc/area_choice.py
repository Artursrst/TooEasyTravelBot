from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import CallbackQuery

def area_markup(areas:list) -> CallbackQuery:
    '''
    Функция для создания кнопок с выбором района

    :param areas: список районов
    :return: информация с выбранным пользователем районом
    '''
    destinations = InlineKeyboardMarkup()

    for area in areas:
        destinations.add(InlineKeyboardButton(text=area[0],
                          callback_data='ar'+area[1]))
    return destinations
