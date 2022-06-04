from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def request() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Отправить данные', request_contact=True))
    return keyboard