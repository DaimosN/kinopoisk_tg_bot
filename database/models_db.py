from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime


sqlite_database = "sqlite:///chat_bot.db"

engine = create_engine(sqlite_database)
engine.connect()

class Base(DeclarativeBase):
    """Базовая модель, в который определены два столбца
    id - уникальный идентификатор
    created_on - дата создания записи
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_on = Column(DateTime, default=datetime.now())


class History(Base):
    """Модель, которая хранит историю поиска"""
    __tablename__ = "log_table"

    id_user = Column(Integer, nullable=False)
    tg_nickname = Column(String, nullable=False)
    command_name = Column(String, nullable=True)
    movie_name = Column(String, nullable=True)
    released = Column(Integer, nullable=True)
    movie_type = Column(String, nullable=True)
    movie_genre = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)

