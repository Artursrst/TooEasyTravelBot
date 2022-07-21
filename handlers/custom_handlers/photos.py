from states.My_States import MyStates
from keyboards.reply.request_info import request_to_api
from keyboards.reply.high_n_low_price_rec import info_for_high_and_low_price
from keyboards.reply.reclabel import get_mainlabel
from loader import bot
import json
from database.appeals_to_bd import *
from telebot.types import Message

@bot.message_handler(state=MyStates.photos)
def q_results_handler(message: Message) -> None:
    if message.text.isdigit() and 0 <= len(message.text) < 6:
        with db:
            dop = User.select().where(User.telegram_id == message.from_user.id).get()
            r_dop = S_request.get(
                S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                S_request.number == len(dop.Requests))
            r_dop.photos = message.text
            r_dop.save()

            if S_request.select().where(S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                                        S_request.number == len(dop.Requests)).get().command == "/bestdeal":
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
                bot.set_state(message.from_user.id, MyStates.distance, message.chat.id)
                bot.send_message(message.chat.id,
                                 'Введите минимальное и максимальное расстояние от отеля до {} в милях через ";" (Например: 0.3 ; 2.5)'.format(mlabel))
            else:
                bot.set_state(message.from_user.id, None, message.chat.id)
                dop = User.select().where(User.telegram_id == message.from_user.id).get()
                url = "https://hotels4.p.rapidapi.com/properties/list"
                querystring = {"destinationId": "{}".format(
                    S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().area)}
                headers = {
                    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
                    "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
                }
                q_text = json.dumps(request_to_api(url, headers, querystring))

                if S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                                 S_request.number==len(dop.Requests)).get().command == '/highprice':
                    label_info, distance_info, price_info, address_info, name_info = info_for_high_and_low_price(q_text, S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().q_results, 'h')
                elif S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                                 S_request.number==len(dop.Requests)).get().command == '/lowprice':
                    label_info, distance_info, price_info, address_info, name_info = info_for_high_and_low_price(q_text, S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().q_results, 'l')

                bot.send_message(message.chat.id,
                                 'Отели по вашему запросу: ')
                for q in range(len(distance_info)):
                    bot.send_message(message.chat.id, 'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {} миль\nЦена за день: {}$\n'.format(name_info[q], address_info[q], label_info, distance_info[q], price_info[q]))
                bot.send_message(message.chat.id, 'К сожалению фотографии на данный момент недоступны')
    else:
        bot.send_message(message.chat.id,
                         'Введите пожалуйста 1 число от 1 до 6, или 0 если не хотите выводить фотографии')