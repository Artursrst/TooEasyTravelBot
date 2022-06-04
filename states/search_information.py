from telebot.handler_backends import State, StatesGroup

# Город поиска

class UserInfoState(StatesGroup):
    city = State()
