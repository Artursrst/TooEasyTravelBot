from states.My_States import MyStates
from keyboards.reply.price_dist_lab_and_other_rec import info_for_high_and_low_price
from keyboards.reply.reclabel import get_mainlabel
from keyboards.reply.photos_rec import photos_receiving
from loader import bot
from database.appeals_to_bd import *
from telebot.types import Message
from datetime import datetime

@bot.message_handler(state=MyStates.photos)
def q_results_handler(message: Message) -> None:
    if message.text.isdigit() and 0 <= len(message.text) <= 4:
        with bot.retrieve_data(message.from_user.id) as data:
            data['photos'] = message.text

            if data['command'] == "/bestdeal":
                mlabel = get_mainlabel(data['area'])
                bot.set_state(message.from_user.id, MyStates.distance, message.chat.id)
                bot.send_message(message.chat.id,
                                 'Введите минимальное и максимальное расстояние от отеля до {} в милях через ";" (Например: 0.3 ; 2.5)'.format(mlabel))
            else:
                bot.set_state(message.from_user.id, None, message.chat.id)

                if data['command'] == '/highprice':
                    label_info, distance_info, price_info, address_info, name_info, id = info_for_high_and_low_price(data['area'], int(data['q_results']), 'h')
                elif data['command'] == '/lowprice':
                    label_info, distance_info, price_info, address_info, name_info, id = info_for_high_and_low_price(data['area'], int(data['q_results']), 'l')
                if len(distance_info) < int(data['q_results']):
                    bot.send_message(message.chat.id,
                                     'По вашему запросу в нашей базе данных всего {} отелей'.format(len(distance_info)))
                bot.send_message(message.chat.id,
                                 'Отели по вашему запросу: ')
                for q in range(len(distance_info)):
                    bot.send_message(message.chat.id, 'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}:  {} миль\nЦена за день: {}\n'.format(name_info[q], address_info[q], label_info, distance_info[q], price_info[q]))
                    if data['photos'] == 0:
                        continue
                    photos = photos_receiving(int(id[q]), int(data['photos']))
                    for e in range(len(photos)):
                        try:
                            print(photos[e])
                            bot.send_photo(message.chat.id, '{}'.format(photos[e]))
                        except Exception:
                            print(Exception)
                            print(photos[e])

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
                                         number=i, command=data['command'], r_date=datetime.now(), q_results=data['q_results'], area=data['area'], photos=data['photos'])
                        break

    else:
        bot.send_message(message.chat.id,
                         'Введите пожалуйста 1 число от 1 до 4, или 0 если не хотите выводить фотографии')