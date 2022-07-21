from states.My_States import MyStates
from keyboards.reply.request_info import request_to_api
from loader import bot
import json
from database.appeals_to_bd import *
from telebot.types import Message


@bot.message_handler(state=MyStates.q_results)
def q_results_handler(message: Message) -> None:
    if message.text.isdigit() and 0 < len(message.text) < 10:
        bot.set_state(message.from_user.id, MyStates.photos, message.chat.id)

        with db:
            dop = User.select().where(User.telegram_id == message.from_user.id).get()
            r_dop = S_request.get(
                S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                S_request.number == len(dop.Requests))
            r_dop.q_results = message.text
            r_dop.save()

        bot.send_message(message.chat.id,
                         'Введите количество выводимых фотографий(не больше 6) или 0 если не хотите смотреть фотографии')
    else:
        bot.send_message(message.chat.id,
                         'Неправильно введены данные, напишите число от 1 до 10')