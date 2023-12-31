from states.My_States import MyStates
from loader import bot
from telebot.types import Message

@bot.message_handler(state=MyStates.q_results)
def q_results_handler(message: Message) -> None:
    '''
    Хендлер для получения информации о том сколько вариантов отелей нужно вывести пользователю,
    так же продолжает сценарий поиска повторным запросом даты

    :param message: информация от пользователя
    :return: None
    '''

    if message.text.isdigit() and 0 < int(message.text) < 10:
        bot.set_state(message.from_user.id, MyStates.photos, message.chat.id)

        with bot.retrieve_data(message.from_user.id) as data:
            data['q_results'] = message.text

        bot.send_message(message.from_user.id,
                         'Введите количество выводимых фотографий(не больше 4) '
                         'или 0 если не хотите смотреть фотографии')
    else:
        bot.send_message(message.chat.id,
                         'Неправильно введены данные, напишите число от 1 до 10')