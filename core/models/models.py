from peewee import (Model,
                    CharField,
                    ForeignKeyField,
                    DateTimeField,
                    SqliteDatabase)

DB = SqliteDatabase('chat.db')

class UserModel(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DB
        table_name = 'users'


class MessageModel(Model):
    message = CharField()
    sender = ForeignKeyField(
        model=UserModel,
        backref='messages',
        on_delete='CASCADE',
        on_update='CASCADE'
    )
    time_sent = DateTimeField()

    class Meta:
        database = DB
        table_name = 'messages'


DB.connect()
DB.create_tables([UserModel, MessageModel])