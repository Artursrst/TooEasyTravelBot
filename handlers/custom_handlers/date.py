from states.My_States import MyStates
from loader import bot
from telebot.types import CallbackQuery
from utils.misc.calendar import create_calendar

@bot.callback_query_handler(state=MyStates.date, func=None)
def date_handler(callback_query: CallbackQuery):
    '''
    Хендлер для получения информации о том когда пользователь планирует заселиться в отель,
    так же продолжает сценарий поиска вопросом о том сколько вариантов отелей нужно вывести пользователю

    :param callback_query: информация о выборе пользователя
    :return: None
    '''

    result, keyboard, step = create_calendar(callback_query, is_process=True)

    if not result and keyboard:
        bot.edit_message_text(f'Укажите {step} заезда',
                              callback_query.from_user.id,
                              callback_query.message.message_id,
                              reply_markup=keyboard)

    elif result:
        with bot.retrieve_data(callback_query.from_user.id) as data:
            data['date'] = result

        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

        calendar, step = create_calendar(callback_query)
        bot.send_message(callback_query.from_user.id, f"Повторите {step} заезда", reply_markup=calendar)

        bot.set_state(callback_query.from_user.id, MyStates.sdate, callback_query.message.chat.id)