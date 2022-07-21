from states.My_States import MyStates
from keyboards.reply.request_info import request_to_api
from loader import bot
import json
from database.appeals_to_bd import *
from telebot.types import Message
import re

#Проверка попадают ли введённые числа в диапазоны

@bot.message_handler(state=MyStates.date)
def date_handler(message: Message) -> None:
    pattern = r'\.'
    text = re.split(pattern, message.text)
    if len(text) == 3:
        if (text[0].isdigit() and 0 < len(text[0]) < 3) and (text[1].isdigit() and 0 < len(text[1]) < 3) and (text[2].isdigit() and len(text[2]) == 4):
            if (0 >= int(text[0]) > 31) or (0 >= int(text[1]) > 12) or (2021 >= int(text[2]) > 2025):
                bot.send_message(message.chat.id,
                                 'Дата введена в неправильном формате, введите дату в формате: день число от 1 до 31, месяц от 1 до 12, год от 2022 до 2025')
            else:

                bot.set_state(message.from_user.id, MyStates.q_results, message.chat.id)

                with db:
                    dop = User.select().where(User.telegram_id == message.from_user.id).get()
                    r_dop = S_request.get(
                        S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                        S_request.number == len(dop.Requests))
                    r_dop.date = message.text
                    r_dop.save()

                bot.send_message(message.chat.id,
                                 'Введите количество выводимых вариантов(не больше 10)')
        else:
            bot.send_message(message.chat.id,
                             'Дата введена в неправильном формате, введите дату в формате: день.месяц.год (Например: 03.07.2023)')
    else:
        bot.send_message(message.chat.id,
                         'Дата введена в неправильном формате, введите дату в формате: день.месяц.год (Например: 03.07.2023)')
