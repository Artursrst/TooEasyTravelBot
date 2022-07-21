from states.My_States import MyStates
from keyboards.reply.request_info import request_to_api
from loader import bot
import json
from database.appeals_to_bd import *
from telebot.types import Message
import re
from keyboards.reply.reclabel import get_mainlabel
from keyboards.reply.high_n_low_price_rec import info_for_high_and_low_price

@bot.message_handler(commands=['history'])
def start(message: Message) -> None:
    with db:
        dop = User.select().where(User.telegram_id == message.from_user.id).get()
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"destinationId": "{}".format(
            S_request.select().where(S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                                     S_request.number == len(dop.Requests)).get().area)}
        headers = {
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
            "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
        }
        q_text = json.dumps(request_to_api(url, headers, querystring))
        bot.send_message(message.chat.id, 'Данные по вашим последним 10 запросам: ')
        for R in dop.Requests:
            if R.command == '/highprice' or R.command == '/lowprice':
                if R.command == '/highprice':
                    label_info, distance_info, price_info, address_info, name_info = info_for_high_and_low_price(q_text, S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().q_results, 'h')

                elif R.command == '/lowprice':
                    label_info, distance_info, price_info, address_info, name_info = info_for_high_and_low_price(q_text, S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().q_results, 'l')

                for q in range(len(distance_info)):
                    bot.send_message(message.chat.id, 'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {} миль\nЦена за день: {}$\n'.format(name_info[q], address_info[q], label_info, distance_info[q], price_info[q]))
                bot.send_message(message.chat.id, 'К сожалению фотографии на данный момент недоступны')

            elif R.command == '/bestdeal':
                pattern = r';'
                text_w_d = re.split(pattern, S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().distance)
                text_w_c = re.split(pattern, S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().cost)

                label_info, distance_info, price_info, address_info, name_info = info_for_high_and_low_price(q_text, 19, 'l')
                r_distance_info, r_price_info, r_address_info, r_name_info = [], [], [], []
                bot.set_state(message.from_user.id, None, message.chat.id)

                for i in range(len(distance_info)):
                    if (float(text_w_d[0]) < float(distance_info[i]) < float(text_w_d[1])) and (
                            float(text_w_c[0]) < float(price_info[i][1:]) < float(text_w_c[1])):
                        r_distance_info.append(distance_info[i])
                        r_price_info.append(price_info[i])
                        r_address_info.append(address_info[i])
                        r_name_info.append(name_info[i])
                if len(r_distance_info) == 0:
                    bot.send_message(message.chat.id,
                                     'К сожалению отели удовлетворяющие вашему запросу отсутствуют в нашей базе данных')
                else:
                    q_r = S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().q_results
                    for q in range(len(r_distance_info)):
                        bot.send_message(message.chat.id,
                                         'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {} миль\nЦена за день: {}$\n'.format(
                                             r_name_info[q], r_address_info[q], label_info, r_distance_info[q],
                                             r_price_info[q]))
                    if len(r_distance_info) < q_r:
                        bot.send_message(message.chat.id,
                                         'В нашей базе данных всего {} отелей удовлетворяющих вашему запросу'.format(
                                             len(r_distance_info)))
                    bot.send_message(message.chat.id, 'К сожалению фотографии на данный момент недоступны')