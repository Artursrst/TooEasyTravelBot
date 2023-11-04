from datetime import date
from telegram_bot_calendar import DetailedTelegramCalendar
from telebot.types import CallbackQuery

ALL_STEPS = {'y': 'год', 'm': 'месяц', 'd': 'день'}

def create_calendar(callback_data:CallbackQuery, min_date:str=None, is_process:bool=None, locale:str='ru') -> list:
    '''
    Функция для создания календаря, чтобы пользователь мог выбрать дату заезда в отель

    :param callback_data: значение keyboard до конца процесса выбора
    :param min_date: минимальная дата в календаре
    :param is_process: True or False
    :param locale: выбор языка
    :return: информация о шага выполнения выбора даты, и выбранная дата
    '''
    if min_date is None:
        min_date = date.today()

    if is_process:
        result, keyboard, step = DetailedTelegramCalendar(min_date=min_date, locale=locale).process(call_data=callback_data.data)
        return result, keyboard, ALL_STEPS[step]
    else:
        calendar, step = DetailedTelegramCalendar(current_date=min_date,
                                         min_date=min_date,
                                         locale=locale).build()
        return calendar, ALL_STEPS[step]