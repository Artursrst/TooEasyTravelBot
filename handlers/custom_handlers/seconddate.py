from states.My_States import MyStates
from loader import bot
from telebot.types import CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

@bot.callback_query_handler(func=DetailedTelegramCalendar.func(), state=MyStates.sdate)
def sdate_handler(callback_query: CallbackQuery):
    '''
    Хендлер для повторного получения информации о том когда пользователь планируется заселиться в отель

    :param callback_query: инфомарция о выборе пользователя
    :return: None
    '''

    result, key, step = DetailedTelegramCalendar().process(callback_query.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              callback_query.message.chat.id,
                              callback_query.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(callback_query.from_user.id) as data:
            data['date'] = result

        bot.edit_message_text(f"Вы выбрали {result}",
                              callback_query.message.chat.id,
                              callback_query.message.message_id)
        bot.set_state(callback_query.from_user.id, MyStates.photos, callback_query.message.chat.id)
        bot.send_message(callback_query.message.chat.id,
                         'Введите количество выводимых фотографий(не больше 4) '
                         'или 0 если не хотите смотреть фотографии')