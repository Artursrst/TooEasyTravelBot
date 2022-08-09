from loader import bot
from database.appeals_to_bd import *
from telebot.types import Message
import re
from utils.misc.info import whole_info
from utils.misc.photos_rec import photos_receiving
import requests

@bot.message_handler(commands=['history'])
def start(message: Message) -> None:
    '''
    Хендлер для команды вывода истории поиска пользователю, также осуществляет вывод информации пользователю

    :param message: информация от пользователя
    :return: None
    '''

    with db:
        dop = User.select().where(User.telegram_id == message.from_user.id).get()
        bot.send_message(message.chat.id, 'Данные по вашим последним 10 запросам: ')
        for R in dop.Requests:
            if R.command == '/highprice' or R.command == '/lowprice': #Получение информации из базы данных для команд /lowprice и /highprice
                if R.command == '/highprice':
                    label_info, distance_info, price_info, address_info, name_info, id = whole_info(S_request.select().where(
                        S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                        S_request.number == len(dop.Requests)).get().area, int(S_request.select().where(
                        S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                        S_request.number==len(dop.Requests)).get().q_results), 'h')

                elif R.command == '/lowprice':
                    label_info, distance_info, price_info, address_info, name_info, id = whole_info(S_request.select().where(
                        S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                        S_request.number == len(dop.Requests)).get().area, int(S_request.select().where(
                        S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                        S_request.number==len(dop.Requests)).get().q_results), 'l')

                for q, val in enumerate(distance_info): #Вывод информации пользователю
                    bot.send_message(message.chat.id, 'Название отеля: {}\n'
                                                      'Ссылка на отель: hotels.com/ho{}\n'
                                                      'Адрес отеля: {}\n'
                                                      'Расстояние до {}: {} миль\n'
                                                      'Цена за день: {}$\n'.format(
                                                       name_info[q], id[q], address_info[q],
                                                       label_info, val,
                                                       price_info[q]))
                    if S_request.select().where(
                            S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                            S_request.number==len(dop.Requests)).get().q_results == 0:
                        continue
                    photos = photos_receiving(int(id[q]), int(S_request.select().where(S_request.user==User.select().where(
                        User.telegram_id == message.from_user.id),
                        S_request.number==len(dop.Requests)).get().photos))
                    for e in photos:
                        response = requests.get(e)
                        bot.send_photo(message.chat.id, response.content)


            elif R.command == '/bestdeal': #Получение информации из базы данных для команды /bestdeal
                pattern = r';'
                text_w_d = re.split(pattern, S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().distance)
                text_w_c = re.split(pattern, S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().cost)
                label_info, distance_info, price_info, address_info, name_info, id = whole_info(
                    S_request.select().where(
                        S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                        S_request.number == len(dop.Requests)).get().area, 19, 'l')
                r_distance_info, r_price_info, r_address_info, r_name_info, r_id = [], [], [], [], []
                bot.set_state(message.from_user.id, None, message.chat.id)

                for i, val in enumerate(distance_info):
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
                    q_r = int(S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().q_results)

                    if len(r_distance_info) < q_r:
                        bot.send_message(message.chat.id,
                                         'В нашей базе данных всего {} '
                                         'отелей удовлетворяющих вашему запросу'.format(
                                          len(r_distance_info)))

                    for q, val in enumerate(r_distance_info): #Вывод информации пользователю
                        bot.send_message(message.chat.id,
                                         'Название отеля: {}\n'
                                         'Ссылка на отель: hotels.com/ho{}\n'
                                         'Адрес отеля: {}\n'
                                         'Расстояние до {}: {}  миль\n'
                                         'Цена за день: {}\n'.format(
                                             r_name_info[q], id[q], r_address_info[q], label_info, val,
                                             r_price_info[q]))
                        if S_request.select().where(
                                S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                                S_request.number == len(dop.Requests)).get().q_results == 0:
                            continue
                        photos = photos_receiving(int(r_id[q]), int(S_request.select().where(
                            S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                            S_request.number == len(dop.Requests)).get().photos))
                        for e in photos:
                            response = requests.get(e)
                            bot.send_photo(message.chat.id, response.content)



