from keyboards.reply.city_choice import city_markup
from loader import bot
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
