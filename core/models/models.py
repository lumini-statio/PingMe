import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker,\
                        relationship,\
                        declarative_base


engine = sa.create_engine("sqlite:///chat_android.db")

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String)
    password = sa.Column(sa.String)
    messages = relationship("MessageModel", backref='user')


class MessageModel(Base):
    __tablename__ = 'messages'

    id = sa.Column(sa.Integer, primary_key=True)
    message = sa.Column(sa.String)
    time_sent = sa.Column(sa.DateTime)
    sender = sa.Column(sa.Integer, sa.ForeignKey('users.id'))


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
