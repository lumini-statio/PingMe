from peewee import Model, CharField, ForeignKeyField


class UserModel(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = 'sqlite:///chat.db'
        table_name = 'users'


class MessegeModel(Model):
    message = CharField()
    sender = ForeignKeyField(
        model=UserModel,
        backref='messages',
        on_delete='CASCADE',
        on_update='CASCADE'
    )
    time_sent = CharField()

    class Meta:
        database = 'sqlite:///chat.db'
        table_name = 'messages'