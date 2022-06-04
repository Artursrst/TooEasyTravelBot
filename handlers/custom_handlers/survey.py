from keyboards.reply.contact import request
from loader import bot
from states.search_information import UserInfoState
from telebot.types import Message
from string import ascii_letters

def is_Latin(text:str) -> bool:
    for l in text:
        print(l, l in ascii_letters)
        if l not in ascii_letters:
            return False
    return True

@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.username}, введи город в котором хочешь посмотреть отели')


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    if is_Latin(message.text):
        bot.send_message(message.from_user.id, 'Спасибо, записал, отправь информацию нажав на кнопку', reply_markup=request())

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Название города должно быть написано английскими буквами')