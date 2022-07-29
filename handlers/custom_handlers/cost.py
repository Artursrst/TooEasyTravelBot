from states.My_States import MyStates
from loader import bot
from telebot.types import Message
import re
from keyboards.reply.reclabel import get_mainlabel
from keyboards.reply.price_dist_lab_and_other_rec import info_for_high_and_low_price
from keyboards.reply.photos_rec import photos_receiving
from database.appeals_to_bd import *
from datetime import datetime

@bot.message_handler(state=MyStates.cost)
def q_results_handler(message: Message) -> None:
    pattern = r';'
    text_w_c = re.split(pattern, message.text)

    try:
        if len(text_w_c) != 2:
            raise Exception
        float(text_w_c[0])
        float(text_w_c[1])
    except Exception:
        with bot.retrieve_data(message.from_user.id) as data:
            mlabel = get_mainlabel(data['area'])
            bot.send_message(message.chat.id,
                             'Данные введены в неправильном формате\nВведите минимальное и максимальное расстояние от отеля до {} в милях через ";" (Например: 0.3 ; 20)'.format(
                                 mlabel))
    with bot.retrieve_data(message.from_user.id) as data:
        data['cost'] = message.text
        pattern = r';'
        text_w_d = re.split(pattern, data['distance'])
        q_r = int(data['q_results'])
        label_info, distance_info, price_info, address_info, name_info, id = info_for_high_and_low_price(data['area'], 19, 'l')

        r_distance_info, r_price_info, r_address_info, r_name_info, r_id = [], [], [], [], []
        bot.set_state(message.from_user.id, None, message.chat.id)
        with db:
            if not User.select().where(User.telegram_id == message.from_user.id):
                User.create(name=message.from_user.full_name, telegram_id=message.from_user.id)

            dop = User.select().where(User.telegram_id == message.from_user.id).get()
            if len(dop.Requests) == 10:
                S_request.select().where(
                    S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                    S_request.number == 1).get().delete_instance()
                n = 1
                for R in dop.Requests:
                    R.number = n
                    n += 1
                    R.save()

            for i in range(1, 11):
                if S_request.select().where(
                        S_request.user == User.select().where(
                            User.telegram_id == message.from_user.id and User.name == message.from_user.full_name),
                        S_request.number == i):
                    continue
                S_request.create(user=User.select().where(
                    User.telegram_id == message.from_user.id and User.name == message.from_user.full_name),
                    number=i, command=data['command'], r_date=datetime.now(), q_results=data['q_results'], area=data['area'],
                            photos=data['photos'], cost=data['cost'], distance=data['distance'])
                break

        for i in range(len(distance_info)):
            if (float(text_w_d[0]) < float(distance_info[i]) < float(text_w_d[1])) and (float(text_w_c[0]) < float(price_info[i][1:]) < float(text_w_c[1])):
                r_distance_info.append(distance_info[i])
                r_price_info.append(price_info[i])
                r_address_info.append(address_info[i])
                r_name_info.append(name_info[i])
                r_id.append(id[i])
        if len(r_distance_info) == 0:
            bot.send_message(message.chat.id,
                             'К сожалению отели удовлетворяющие вашему запросу отсутствуют в нашей базе данных')
        else:
            if len(r_distance_info) < q_r:
                bot.send_message(message.chat.id, 'В нашей базе данных всего {} отелей удовлетворяющих вашему запросу'.format(len(r_distance_info)))
            elif len(r_distance_info) > q_r:
                r_name_info = r_name_info[:q_r]
                r_address_info = r_address_info[:q_r]
                r_distance_info = r_distance_info[:q_r]
                r_price_info = r_price_info[:q_r]
                r_id = r_id[:q_r]
                for q in range(len(r_distance_info)):
                    bot.send_message(message.chat.id,
                                     'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {} миль\nЦена за день: {}$\n'.format(
                                         r_name_info[q], r_address_info[q], label_info, r_distance_info[q], r_price_info[q]))
                    if data['photos'] == 0:
                        continue
                    photos = photos_receiving(int(r_id[q]), int(data['photos']))
                    for e in range(len(photos)):
                        bot.send_photo(message.chat.id, '{}'.format(photos[e]))
            else:
                for q in range(len(r_distance_info)):
                    bot.send_message(message.chat.id,
                                     'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {} миль\nЦена за день: {}$\n'.format(
                                         r_name_info[q], r_address_info[q], label_info, r_distance_info[q], r_price_info[q]))

                    if data['photos'] == 0:
                        continue
                    photos = photos_receiving(int(r_id[q]), int(data['photos']))
                    for e in range(len(photos)):
                        try:
                            photos[e]
                            bot.send_photo(message.chat.id, '{}'.format(photos[e]))
                        except Exception:
                            print(Exception)
                            photos[e]