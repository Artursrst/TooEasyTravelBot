from states.My_States import MyStates
from loader import bot
from telebot.types import Message
from utils.misc.reclabel import get_mainlabel
from utils.misc.other import is_float

@bot.message_handler(state=MyStates.distance)
def q_results_handler(message: Message) -> None:
    '''
    Хендлер для получения информации о желаемой минимальной и максимальной дистанции до отеля,
    так же продолжает сценарий поиска вопросом о желаемой стоимости за ночь

    :param message: информация от пользователя
    :return: None
    '''

    text = message.text.split(';')
    if (len(text) == 2) and is_float(text[0]) and is_float(text[1]):
        with bot.retrieve_data(message.from_user.id) as data:
            data['distance'] = message.text
        bot.set_state(message.from_user.id, MyStates.cost, message.chat.id)
        bot.send_message(message.chat.id,
                         'Введите минимальную и максимальную стоиомтсть отеля за ночь в $ ";" (Например: 0.3 ; 70)')
    else:
        with bot.retrieve_data(message.from_user.id) as data:
            mlabel = get_mainlabel(data['area'])
            bot.send_message(message.chat.id,
                             'Данные введены в неправильном формате\n'
                             'Введите минимальное и максимальное расстояние от отеля до '
                             '{} в милях через ";" (Например: 0.3;20)'.format(mlabel))