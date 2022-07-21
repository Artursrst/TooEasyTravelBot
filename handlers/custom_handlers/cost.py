from states.My_States import MyStates
from keyboards.reply.request_info import request_to_api
from loader import bot
import json
from database.appeals_to_bd import *
from telebot.types import Message
import re
from keyboards.reply.reclabel import get_mainlabel
from keyboards.reply.high_n_low_price_rec import info_for_high_and_low_price

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
        with db:
            dop = User.select().where(User.telegram_id == message.from_user.id).get()
            url = "https://hotels4.p.rapidapi.com/properties/list"
            querystring = {"destinationId": "{}".format(
                S_request.select().where(
                    S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                    S_request.number == len(dop.Requests)).get().area)}
            headers = {
                "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
                "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
            }
            q_text = json.dumps(request_to_api(url, headers, querystring))
            mlabel = get_mainlabel(q_text)
            bot.send_message(message.chat.id,
                             'Данные введены в неправильном формате\nВведите минимальное и максимальное расстояние от отеля до {} в милях через ";" (Например: 0.3 ; 20)'.format(
                                 mlabel))

    with db:
        dop = User.select().where(User.telegram_id == message.from_user.id).get()
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {"destinationId": "{}".format(
            S_request.select().where(
                S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                S_request.number == len(dop.Requests)).get().area)}
        headers = {
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
            "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
        }
        q_text = json.dumps(request_to_api(url, headers, querystring))
        r_dop = S_request.get(S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                              S_request.number == len(dop.Requests))
        r_dop.cost = message.text
        r_dop.save()
        pattern = r';'
        text_w_d = re.split(pattern, r_dop.distance)
        q_r = S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().q_results
        label_info, distance_info, price_info, address_info, name_info = info_for_high_and_low_price(q_text, 19, 'l')

        r_distance_info, r_price_info, r_address_info, r_name_info = [], [], [], []
        bot.set_state(message.from_user.id, None, message.chat.id)

        for i in range(len(distance_info)):
            if (float(text_w_d[0]) < float(distance_info[i]) < float(text_w_d[1])) and (float(text_w_c[0]) < float(price_info[i][1:]) < float(text_w_c[1])):
                r_distance_info.append(distance_info[i])
                r_price_info.append(price_info[i])
                r_address_info.append(address_info[i])
                r_name_info.append(name_info[i])
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
                for q in range(len(r_distance_info)):
                    bot.send_message(message.chat.id,
                                     'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {} миль\nЦена за день: {}$\n'.format(
                                         r_name_info[q], r_address_info[q], label_info, r_distance_info[q], r_price_info[q]))
                bot.send_message(message.chat.id, 'К сожалению фотографии на данный момент недоступны')
            else:
                for q in range(len(r_distance_info)):
                    bot.send_message(message.chat.id,
                                     'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {} миль\nЦена за день: {}$\n'.format(
                                         r_name_info[q], r_address_info[q], label_info, r_distance_info[q], r_price_info[q]))

                bot.send_message(message.chat.id, 'К сожалению фотографии на данный момент недоступны')