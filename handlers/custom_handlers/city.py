from loader import bot
from telebot.types import Message
from utils.misc.request_info import caption_id
from utils.misc.area_choice import area_markup
from states.My_States import MyStates
from utils.misc.city_check import city_ch

@bot.message_handler(state=MyStates.city)
def city_handler(message: Message) -> None:
    '''
    Хендлер для получения информации о том в каком городе происхоодит поиск отелей,
    так же продолжает сценарий поиска запросом выбора выбора района

    :param message: информация от пользователя
    :return: None
    '''

    if city_ch(message.text):
        areas = caption_id(message.text)
        if areas:
            bot.send_message(message.from_user.id, 'Выберете район в которым хотите найти отель:',
                             reply_markup=area_markup(areas))
            with bot.retrieve_data(message.from_user.id) as data:
                data['city'] = message.text
        else:
            bot.send_message(message.from_user.id, 'К сожалению в нашей базе данных'
                                                   'отсутствуют данных об отелях этого '
                                                   'города')
            bot.set_state(message.from_user.id, None)

    else:
        bot.send_message(message.from_user.id, 'Город введёт в неправильном формате)')
        bot.send_message(message.from_user.id, 'Введите название города, в котором хотите'
                                               'найти отель, маленькими латинскими буквами,'
                                               ' разделяя слова пробелом (Пример: new york)')