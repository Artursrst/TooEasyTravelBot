from states.My_States import MyStates
from loader import bot
from telebot.types import CallbackQuery
from utils.misc.calendar import create_calendar

@bot.callback_query_handler(state=MyStates.sdate, func=None)
def sdate_handler(callback_query: CallbackQuery):
    '''
    Хендлер для повторного получения информации о том когда пользователь планируется заселиться в отель

    :param callback_query: инфомарция о выборе пользователя
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
        bot.edit_message_text(f"Вы выбрали {result}",
                              callback_query.message.chat.id,
                              callback_query.message.message_id)

        bot.set_state(callback_query.from_user.id, MyStates.q_results, callback_query.message.chat.id)
        bot.send_message(callback_query.message.chat.id,
                         'Введите количество выводимых вариантов(не больше 10)')
