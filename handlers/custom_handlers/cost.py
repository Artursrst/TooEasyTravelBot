from states.My_States import MyStates
from loader import bot
from telebot.types import Message
import re
from utils.misc.reclabel import get_mainlabel
from utils.misc.info import whole_info
from utils.misc.photos_rec import photos_receiving
from utils.misc.dboperations import dbwrite

@bot.message_handler(state=MyStates.cost)
def cost_handler(message: Message) -> None:
    '''
    Хендел для получения информации о желаемой минимальной и максимальной стоимости
    в отелях за ночь, так же в нём осуществляется вывод информации об отелях
    пользователю и запись информации в базу данных

    :param message: инфомарция от пользователя
    :return: None
    '''

    pattern = r';'
    text_w_c = re.split(pattern, message.text)

    try: #Проверка на соответствие введённых пользователем данных заданным параметрам
        if len(text_w_c) != 2:
            raise Exception
        float(text_w_c[0])
        float(text_w_c[1])
    except Exception:
        with bot.retrieve_data(message.from_user.id) as data:
            mlabel = get_mainlabel(data['area'])
            bot.send_message(message.chat.id,
                             'Данные введены в неправильном формате\n'
                             'Введите минимальное и максимальное расстояние от отеля до {}'
                             ' в милях через ";" (Например: 0.3 ; 20)'.format(mlabel))
            
    with bot.retrieve_data(message.from_user.id) as data:
        data['cost'] = message.text
        pattern = r';'
        text_w_d = re.split(pattern, data['distance'])
        q_r = int(data['q_results'])
        label_info, distance_info, price_info, address_info, name_info, id = whole_info(data['area'], 19, 'l') #Получение информации из базы данных

        r_distance_info, r_price_info, r_address_info, r_name_info, r_id = [], [], [], [], []
        bot.set_state(message.from_user.id, None, message.chat.id)
        dbwrite(message.from_user.id, message.from_user.full_name, data['command'], data['q_results'], data['area'],
                data['photos']) #Запись информации в базу данных

        for i, val in enumerate(distance_info): #Вывод пользователю
            if (float(text_w_d[0]) < float(val) < float(text_w_d[1])) and (float(text_w_c[0]) < float(price_info[i][1:]) < float(text_w_c[1])):
                r_distance_info.append(val)
                r_price_info.append(price_info[i])
                r_address_info.append(address_info[i])
                r_name_info.append(name_info[i])
                r_id.append(id[i])
        if len(r_distance_info) == 0:
            bot.send_message(message.chat.id,
                             'К сожалению отели удовлетворяющие вашему запросу отсутствуют в нашей базе данных')
        else:
            if len(r_distance_info) < q_r:
                bot.send_message(message.chat.id, 'В нашей базе данных всего {} '
                                                  'отелей удовлетворяющих вашему запросу'.format(len(r_distance_info)))
            elif len(r_distance_info) > q_r:
                r_name_info = r_name_info[:q_r]
                r_address_info = r_address_info[:q_r]
                r_distance_info = r_distance_info[:q_r]
                r_price_info = r_price_info[:q_r]
                r_id = r_id[:q_r]
                for q, val in enumerate(r_distance_info):
                    bot.send_message(message.chat.id,
                                     'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {} миль\nЦена за день: {}$\n'.format(
                                         r_name_info[q], r_address_info[q], label_info, val, r_price_info[q]))
                    if data['photos'] == 0:
                        continue
                    photos = photos_receiving(int(r_id[q]), int(data['photos']))
                    for e in photos:
                        bot.send_photo(message.chat.id, '{}'.format(e))
            else:
                for q, val in enumerate(r_distance_info):
                    bot.send_message(message.chat.id,
                                     'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {} миль\nЦена за день: {}$\n'.format(
                                         r_name_info[q], r_address_info[q], label_info, val, r_price_info[q]))

                    if data['photos'] == 0:
                        continue
                    photos = photos_receiving(int(r_id[q]), int(data['photos']))
                    for e in photos:
                        bot.send_photo(message.chat.id, '{}'.format(e))