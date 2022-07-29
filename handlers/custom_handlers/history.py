from loader import bot
from database.appeals_to_bd import *
from telebot.types import Message
import re
from keyboards.reply.price_dist_lab_and_other_rec import info_for_high_and_low_price
from keyboards.reply.photos_rec import photos_receiving

@bot.message_handler(commands=['history'])
def start(message: Message) -> None:
    with db:
        dop = User.select().where(User.telegram_id == message.from_user.id).get()
        bot.send_message(message.chat.id, 'Данные по вашим последним 10 запросам: ')
        for R in dop.Requests:
            if R.command == '/highprice' or R.command == '/lowprice':
                if R.command == '/highprice':
                    label_info, distance_info, price_info, address_info, name_info, id = info_for_high_and_low_price(S_request.select().where(S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                                     S_request.number == len(dop.Requests)).get().area, int(S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().q_results), 'h')

                elif R.command == '/lowprice':
                    label_info, distance_info, price_info, address_info, name_info, id = info_for_high_and_low_price(S_request.select().where(S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                                     S_request.number == len(dop.Requests)).get().area, int(S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().q_results), 'l')

                for q in range(len(distance_info)):
                    bot.send_message(message.chat.id, 'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {} миль\nЦена за день: {}$\n'.format(name_info[q], address_info[q], label_info, distance_info[q], price_info[q]))
                    if S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                                 S_request.number==len(dop.Requests)).get().q_results == 0:
                        continue
                    photos = photos_receiving(int(id[q]), int(S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                                 S_request.number==len(dop.Requests)).get().photos))
                    for e in range(len(photos)):
                        try:
                            bot.send_photo(message.chat.id, '{}'.format(photos[e]))
                        except Exception:
                            print(Exception)

            elif R.command == '/bestdeal':
                pattern = r';'
                text_w_d = re.split(pattern, S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().distance)
                text_w_c = re.split(pattern, S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().cost)
                label_info, distance_info, price_info, address_info, name_info, id = info_for_high_and_low_price(
                    S_request.select().where(
                        S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                        S_request.number == len(dop.Requests)).get().area, 19, 'l')
                r_distance_info, r_price_info, r_address_info, r_name_info, r_id = [], [], [], [], []
                bot.set_state(message.from_user.id, None, message.chat.id)

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
                    q_r = int(S_request.select().where(S_request.user==User.select().where(User.telegram_id == message.from_user.id),
                                             S_request.number==len(dop.Requests)).get().q_results)
                    for q in range(len(r_distance_info)):
                        bot.send_message(message.chat.id,
                                         'Название отеля: {}\nАдрес отеля: {}\nРасстояние до {}: {}  миль\nЦена за день: {}\n'.format(
                                             r_name_info[q], r_address_info[q], label_info, r_distance_info[q],
                                             r_price_info[q]))
                        if S_request.select().where(
                                S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                                S_request.number == len(dop.Requests)).get().q_results == 0:
                            continue
                        photos = photos_receiving(int(r_id[q]), int(S_request.select().where(
                            S_request.user == User.select().where(User.telegram_id == message.from_user.id),
                            S_request.number == len(dop.Requests)).get().photos))
                        for e in range(len(photos)):
                            try:
                                print(photos[e])
                                bot.send_photo(message.chat.id, '{}'.format(photos[e]))
                            except Exception:
                                print(Exception)
                                print(photos[e])

                    if len(r_distance_info) < q_r:
                        bot.send_message(message.chat.id,
                                         'В нашей базе данных всего {} отелей удовлетворяющих вашему запросу'.format(
                                             len(r_distance_info)))
