from states.My_States import MyStates
from keyboards.reply.request_info import request_to_api
from loader import bot
import json
from database.appeals_to_bd import *
from telebot.types import Message
import re
from keyboards.reply.reclabel import get_mainlabel
from keyboards.reply.high_n_low_price_rec import info_for_high_and_low_price

#'Введите минимальное и максимальное расстояние от отеля до {} в милях через ";" (Например: 0.3 ; 2.5)
@bot.message_handler(state=MyStates.distance)
def q_results_handler(message: Message) -> None:
    pattern = r';'
    text = re.split(pattern, message.text)

    try:
        if len(text) != 2:
            raise Exception
        float(text[0])
        float(text[1])
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
        r_dop = S_request.get(S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                              S_request.number == len(dop.Requests))
        r_dop.distance = message.text
        r_dop.save()
        bot.set_state(message.from_user.id, MyStates.cost, message.chat.id)
        bot.send_message(message.chat.id,
                         'Введите минимальную и максимальную стоиомтсть отеля за ночь в $ ";" (Например: 0.3 ; 70)')