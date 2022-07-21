from telebot.handler_backends import State, StatesGroup

class MyStates(StatesGroup):
    q_results = State()
    photos = State()
    date = State()
    cost = State()
    distance = State()