from keyboards.reply.city_choice import city_markup
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot
from states.search_information import UserInfoState
from telebot.types import Message, CallbackQuery
from string import ascii_letters

def is_Latin(text:str) -> bool:
    for l in text:
        if l not in ascii_letters:
            return False
    return True

@bot.message_handler(commands=['survey'])
def start(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=city_markup())

@bot.callback_query_handler(lambda y: y.data == 'tuc')
def answer_yes(callback_query: CallbackQuery) -> None:
    print(callback_query.data)


#@bot.message_handler(state=UserInfoState.city)
#def get_city(message: Message) -> None:
#    bot.set_state(message.from_user.id, None, message.chat.id)
#    if is_Latin(message.text):
#        bot.send_message(message.from_user.id, 'Спасибо, записал, отправь информацию нажав на кнопку', reply_markup=request())
#
#        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#            data['city'] = message.text
#    else:
#        bot.send_message(message.from_user.id, 'Название города должно быть написано английскими буквами')