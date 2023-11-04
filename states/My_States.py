from telebot.handler_backends import State, StatesGroup

class MyStates(StatesGroup):
    city = State()
    area = State()
    q_results = State()
    photos = State()
    date = State()
    sdate = State()
    cost = State()
    distance = State()
