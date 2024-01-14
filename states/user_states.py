from telebot.handler_backends import State, StatesGroup


class GetDigitForSearch(StatesGroup):
    digit_of_search = State()


class GetMovieByTitle(StatesGroup):
    """Состояния для команды поиска фильма по названию"""
    movie_name = State()
    count_of_search = State()


class GetRandomMovieWithParams(StatesGroup):
    """Состояния для команды поиска случайного фильма по параметрам"""
    released = State()
    type = State()  # "movie", "tv-series", "!anime"
    genre = State()  # "драма", "комедия", "!мелодрама", "+ужасы"

