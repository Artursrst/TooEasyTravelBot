from keyboards.reply.city_choice import city_markup
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot
from states.search_information import UserInfoState
from telebot.types import Message, CallbackQuery
from database.appeals_to_bd import *
from keyboards.reply.request_info import request_to_api, caption_and_id_receiving
from keyboards.reply.area_choice import area_markup
from states.My_States import MyStates
from datetime import datetime
import json

#Состояния и заполнение базы данных


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def start(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Выберете город в которым хотите найти отель:', reply_markup=city_markup())

    with db:
        if not User.select().where(User.telegram_id == message.from_user.id):
            User.create(name = message.from_user.full_name, telegram_id = message.from_user.id)

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
                    S_request.user == User.select().where(User.telegram_id == message.from_user.id and User.name == message.from_user.full_name),
                    S_request.number == i):
                continue
            S_request.create(user=User.select().where(User.telegram_id == message.from_user.id and User.name == message.from_user.full_name), number=i, command=message.text, r_date=datetime.now())
            break


@bot.callback_query_handler(lambda y: y.data in 'new_york los_angeles chicago houston philadelphia san_antonio dallas san_jose san_francisco')
def area_interview(callback_query: CallbackQuery) -> None:
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": "{}".format(callback_query.data), "locale": "en_US"}
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
    }
    areas = caption_and_id_receiving(json.dumps(request_to_api(url, headers, querystring)))
    bot.send_message(callback_query.from_user.id, 'Выберете район в которым хотите найти отель:', reply_markup=area_markup(areas))
    with db:
        dop = User.select().where(User.telegram_id == callback_query.from_user.id).get()
        r_dop = S_request.get(S_request.user == User.select().where(User.telegram_id == callback_query.from_user.id), S_request.number == len(dop.Requests))
        r_dop.city = callback_query.data
        r_dop.save()

@bot.callback_query_handler(lambda y: 'ar' in y.data)
def date_interview(callback_query: CallbackQuery) -> None:

    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {"destinationId": "{}".format(callback_query.data[2:])}
    headers = {
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
        "X-RapidAPI-Key": "c040a13279msh33671d36277e40fp190802jsn81aad8fc9c57"
    }
    with open('hotels{}.json'.format(callback_query.from_user.id), 'w') as file:
        json.dump(request_to_api(url, headers, querystring), file, indent=4)

    bot.set_state(callback_query.from_user.id, MyStates.date)
    bot.send_message(callback_query.from_user.id, 'Введите дату, когда планируете заселиться в формате: день.месяц.год (Например: 03.07.2023)')

    with db:
        dop = User.select().where(User.telegram_id == callback_query.from_user.id).get()
        r_dop = S_request.get(S_request.user == User.select().where(User.telegram_id == callback_query.from_user.id),
                              S_request.number == len(dop.Requests))
        r_dop.area = callback_query.data[2:]
        r_dop.save()



#Кнопка с выбором города
#Кнопка с выбором района
#Дата
#Количество отелей кроме заранее заданного максимума
#Необходимость вывода фотографий, кроме заранее заданного максимума