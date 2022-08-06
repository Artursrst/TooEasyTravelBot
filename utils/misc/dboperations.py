from database.appeals_to_bd import *
from datetime import datetime

def dbwrite(userid:int, username:str, command:str, q_results:str, area:str, photos:str) -> None:
    '''
    Функция для записи инфомарции в базу данных, и удаления старых запросов

    :param userid(int): ид пользователя
    :param username(str): полное имя пользователя
    :param command(str): команда запроса пользователя
    :param q_results(str): количество выводимых результатов
    :param area(str): район поиска
    :param photos(int): выводить ли фотографии и сколько
    :return: None
    '''

    with db:
        if not User.select().where(User.telegram_id == userid):
            User.create(name=username, telegram_id=userid)

        dop = User.select().where(User.telegram_id == userid).get()
        if len(dop.Requests) == 10:
            S_request.select().where(
                S_request.user == User.select().where(User.telegram_id == userid),
                S_request.number == 1).get().delete_instance()
            n = 1
            for R in dop.Requests:
                R.number = n
                n += 1
                R.save()

        for i in range(1, 11):
            if S_request.select().where(
                    S_request.user == User.select().where(
                        User.telegram_id == userid and User.name == username),
                    S_request.number == i):
                continue
            S_request.create(user=User.select().where(
                User.telegram_id == userid and User.name == username),
                number=i, command=command, r_date=datetime.now(), q_results=q_results,
                area=area, photos=photos)
            break

def dbread():
    pass