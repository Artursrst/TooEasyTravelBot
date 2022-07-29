from states.My_States import MyStates
from loader import bot
from telebot.types import Message
import re

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
                with bot.retrieve_data(message.from_user.id) as data:
                    data['date'] = message.text
                bot.send_message(message.chat.id,
                                 'Введите количество выводимых вариантов(не больше 10)')
        else:
            bot.send_message(message.chat.id,
                             'Дата введена в неправильном формате, введите дату в формате: день.месяц.год (Например: 03.07.2023)')
    else:
        bot.send_message(message.chat.id,
                         'Дата введена в неправильном формате, введите дату в формате: день.месяц.год (Например: 03.07.2023)')
