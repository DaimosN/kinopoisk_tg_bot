from sqlalchemy.orm import Session

from .models_db import History, engine


def _insert_db(id_user: int, user_name: str,  command_name: str = None, movie_name: str = None,
               released: int = None, movie_type: str = None, movie_genre: str = None) -> None:
    with Session(autoflush=False, bind=engine) as db:
        insert_string = History(id_user=id_user, tg_nickname=user_name, command_name=command_name,
                                movie_name=movie_name, released=released, movie_type=movie_type,
                                movie_genre=movie_genre)
        db.add(insert_string)
        db.commit()


def _select_db(limit_flag: str, user_id: int, limit_count: int = None) -> list:
    with Session(autoflush=False, bind=engine) as db:
        if limit_flag == "yes":
            result = db.query(History).filter(History.id_user == user_id).limit(limit_count).all()
        else:
            result = db.query(History).filter(History.id_user == user_id).limit(100).all()
    return result


class SqlCommands():
    @staticmethod
    def insert():
        return _insert_db

    @staticmethod
    def select():
        return _select_db


if __name__ == "__main__":
    _insert_db()
    _select_db()
    SqlCommands()
