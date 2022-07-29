from telebot.handler_backends import State, StatesGroup

class MyStates(StatesGroup):
    command = State()
    city = State()
    area = State()
    q_results = State()
    photos = State()
    date = State()
    cost = State()
    distance = State()
