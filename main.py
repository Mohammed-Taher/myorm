from models import Model
from Field import *
from Database import Database
import datetime

Model.db = Database('database.sqlite')
Model.connection = Model.db.connect()


class Post(Model):
    title = CharField()
    body = TextField()
    created_at = DateTimeField()
    published = BooleanField()


class User(Model):
    first_name = CharField()
    last_name = CharField(max_length=255)
    age = IntegerField()


if __name__ == '__main__':
    post1 = Post()
    post1.title = 'Inheritance In Python'
    post1.body = 'Inheritance is one of the main concepts of OOP.'
    post1.created_at = datetime.datetime.now()
    post1.published = True
    post1.save()
    post1.title = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    post1.save()


    # user2 = User()
    # user2.first_name = 'Mohammed'
    # user2.last_name = 'Taher'
    # user2.age = 30
    # user2.save()
