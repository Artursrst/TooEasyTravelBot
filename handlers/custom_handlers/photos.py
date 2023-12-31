from states.My_States import MyStates
from utils.misc.info import whole_info
from utils.misc.reclabel import get_mainlabel
from utils.misc.photos_rec import photos_receiving
from utils.misc.dboperations import dbwrite
from loader import bot
import requests
from telebot.types import Message

@bot.message_handler(state=MyStates.photos)
def q_results_handler(message: Message) -> None:
    '''
    Хендлер для получения информации о том нужны ли пользователю фотографии и сколько,
    так же осуществляет вывод информации пользователю и запись в базу данных для команд /lowprice и /highprice

    :param message: информация от пользователя
    :return: None
    '''

    if message.text.isdigit() and 0 <= len(message.text) <= 4: #Проверка на соответствие введённых пользователем данных заданным критериям
        with bot.retrieve_data(message.from_user.id) as data:
            data['photos'] = int(message.text)

            if data['command'] == "/bestdeal":
                mlabel = get_mainlabel(data['area'])
                bot.set_state(message.from_user.id, MyStates.distance, message.chat.id)
                bot.send_message(message.chat.id,
                                 'Введите минимальное и максимальное расстояние от отеля до {} '
                                 'в милях через ";" (Например: 0.3;2.5)'.format(mlabel))
            else:
                bot.set_state(message.from_user.id, None, message.chat.id)

                if data['command'] == '/highprice': #Получение информации из базы данных
                    label_info, distance_info, price_info, address_info, name_info, id = whole_info(data['area'], int(data['q_results']), 'h')
                elif data['command'] == '/lowprice':
                    label_info, distance_info, price_info, address_info, name_info, id = whole_info(data['area'], int(data['q_results']), 'l')
                if len(distance_info) < int(data['q_results']):
                    bot.send_message(message.chat.id,
                                     'По вашему запросу в нашей базе данных всего {} отелей'.format(len(distance_info)))
                bot.send_message(message.chat.id,
                                 'Отели по вашему запросу: ')
                for q, val in enumerate(distance_info): #Вывод информации пользователю
                    dz, mz, yz = data['date'].day, data['date'].month, data['date'].year
                    dv, mv, yv = data['sdate'].day, data['sdate'].month, data['sdate'].year
                    wprice = ((dv - dz) * float(price_info[q][1:])) + \
                             ((mv - mz) * 31 * float(price_info[q][1:])) + \
                             ((yv - yz) * 365 * float(price_info[q][1:]))
                    bot.send_message(message.chat.id, 'Название отеля: {}\n'
                                                      'Ссылка на отель: hotels.com/ho{}\n'
                                                      'Адрес отеля: {}\n'
                                                      'Расстояние до {}:  {} миль\n'
                                                      'Цена за день: {}\n'
                                                      'Цена за всё время проживания: ${}'.format(
                                                       name_info[q], id[q], address_info[q], label_info,
                                                       val, price_info[q], wprice))
                    if data['photos'] == 0:
                        continue
                    photos = photos_receiving(int(id[q]), int(data['photos']))
                    for e in photos:
                        response = requests.get(e)
                        bot.send_photo(message.chat.id, response.content)
                #Запись информации в базу данных
                dbwrite(message.from_user.id, message.from_user.full_name, data['command'], data['q_results'], data['area'], data['photos'])

    else:
        bot.send_message(message.chat.id,
                         'Неправильно введены данные, введите число от 1 до 4,'
                         ' или 0 если не хотите выводить фотографии')