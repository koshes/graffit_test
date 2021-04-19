from sqlalchemy import Column, create_engine, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'

    first_name = Column(String(128), nullable=False)
    second_name = Column(String(128), nullable=False)

    user_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
    )

    def __repr__(self):
        return f'{self.first_name} {self.second_name} с {self.user_id} id'


class Log(Base):

    __tablename__ = 'log'

    log_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )

    message = Column(Text)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.user_id'))

    def __repr__(self):
        return f' Лог созданный в {self.created_at} пользователем с {self.user_id} id :: {self.message}'


engine = create_engine('sqlite:///some.db')

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
