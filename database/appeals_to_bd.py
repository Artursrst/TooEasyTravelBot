from peewee import *

db = SqliteDatabase('appeals.db')

class BaseModel(Model):
    '''Базовый класс базы данных'''
    class Meta:
        database = db

class User(BaseModel):
    '''
    Базовый класс, хранящий данные о пользователе

    name(str): полное имя пользователя
    telegram_id(int): id пользователя
    '''
    name = CharField(null=True)
    telegram_id = IntegerField(unique=True)
    class Meta:
        database = db
        order_by = ('telegram_id')

class S_request(Model):
    '''
    Класс, хранящий данные о запросах пользователя

    user(User): информация о том какой пользователь совершин запрос
    number(int): очередность запросов
    city(str): информация о том в каком городе происходит поиск отеля
    area(str): информация о том в каком районе происходит поиск отеля
    command(str): информация о том по какой команде выполнен запрос
    date(str): дата заселения
    photos(int): выводить ли фотографии
    q_results(int): количество вариантов отелей
    r_date(str): дата запроса
    distance(str): максимальная и минимальная дистанция до отеля
    cost(str): максимальная и минимальная цена за ночь
    '''

    user = ForeignKeyField(User, related_name='Requests')
    number = IntegerField(unique=True)
    area = CharField(null=True)
    command = CharField(null=True)
    date = CharField(null=True)
    photos = IntegerField(null=True)
    q_results = IntegerField(null=True)
    r_date = CharField(null=True)
    distance = CharField(null=True)
    cost = CharField(null=True)
    class Meta:
        database = db

def tables_creation() -> None:
    '''Функция для создание базы данных'''
    User.create_table()
    S_request.create_table()

