from keyboards.reply.city_choice import city_markup
from loader import bot
from telebot.types import Message, CallbackQuery
from keyboards.reply.request_info import caption_and_id_receiving
from keyboards.reply.area_choice import area_markup
from states.My_States import MyStates

@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Выберете город в которым хотите найти отель:', reply_markup=city_markup())
    bot.set_state(message.from_user.id, MyStates.command)
    with bot.retrieve_data(message.from_user.id) as data:
        data['command'] = message.text

@bot.callback_query_handler(lambda y: y.data in 'new_york los_angeles chicago houston philadelphia san_antonio dallas san_jose san_francisco')
def area_interview(callback_query: CallbackQuery) -> None:
    bot.set_state(callback_query.from_user.id, MyStates.city)
    areas = caption_and_id_receiving(callback_query.data)
    bot.send_message(callback_query.from_user.id, 'Выберете район в которым хотите найти отель:', reply_markup=area_markup(areas))

    with bot.retrieve_data(callback_query.from_user.id) as data:
        data['city'] = callback_query.data

@bot.callback_query_handler(lambda y: 'ar' in y.data)
def date_interview(callback_query: CallbackQuery) -> None:
    bot.set_state(callback_query.from_user.id, MyStates.area)
    with bot.retrieve_data(callback_query.from_user.id) as data:
        data['area'] = callback_query.data[2:]

    bot.set_state(callback_query.from_user.id, MyStates.date)
    bot.send_message(callback_query.from_user.id, 'Введите дату, когда планируете заселиться в формате: день.месяц.год (Например: 03.07.2023)')