from loader import bot
from telebot.types import CallbackQuery
from states.My_States import MyStates
from utils.misc.calendar import create_calendar

@bot.callback_query_handler(lambda y: 'ar' in y.data)
def area_handler(callback_query: CallbackQuery) -> None:
    '''
    Хендлер для получения информации о том в каком районе происходит поиск отеля,
    так же продолжает сценарий поиска запросом даты, когда пользователь планирует заселиться

    :param callback_query: информация с выбором пользователя
    :return: None
    '''

    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    with bot.retrieve_data(callback_query.from_user.id) as data:
        data['area'] = callback_query.data[2:]

    bot.set_state(callback_query.from_user.id, MyStates.date)

    calendar, step = create_calendar(callback_query)
    bot.send_message(callback_query.from_user.id, f"Укажите {step} заезда", reply_markup=calendar)
