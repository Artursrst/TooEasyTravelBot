from loader import bot
from telebot.types import Message
from states.My_States import MyStates

@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start(message: Message) -> None:
    '''
    Стартовый хендлер для всех 3ёх команд поиска отелей

    :param message: команда введённая пользователем
    :return: None
    '''

    bot.send_message(message.from_user.id, 'Введите название города, в котором хотите'
                                           'найти отель, маленькими латинскими буквами,'
                                           ' разделяя слова пробелом (Пример: new york)')
    bot.set_state(message.from_user.id, MyStates.city)
    with bot.retrieve_data(message.from_user.id) as data:
        data['command'] = message.text