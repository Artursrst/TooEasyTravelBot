from peewee import *
import database

db = SqliteDatabase('appeals.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(null=True)
    telegram_id = IntegerField(unique=True)
    class Meta:
        database = db
        order_by = ('telegram_id')

class S_request(Model):
    user = ForeignKeyField(User, related_name='Requests')
    number = IntegerField(unique=True)
    city = CharField(null=True)
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

def tables_creation():
    User.create_table()
    S_request.create_table()

