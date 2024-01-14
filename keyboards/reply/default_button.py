from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_answer() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_yes = KeyboardButton("Да")
    button_no = KeyboardButton("Нет")
    markup.add(button_yes, button_no)
    return markup


def get_type_movie() -> ReplyKeyboardMarkup:
    movie_button = KeyboardButton('movie')
    series_button = KeyboardButton('tv-series')
    cartoon_button = KeyboardButton('cartoon')
    cartoon_series_button = KeyboardButton('animated-series')
    anime_button = KeyboardButton('anime')

    keyboard = ReplyKeyboardMarkup()
    keyboard.add(movie_button, series_button, cartoon_button, cartoon_series_button, anime_button)

    return keyboard


def get_genres_movie() -> ReplyKeyboardMarkup:
    drama_button = KeyboardButton('драма')
    action_button = KeyboardButton('боевик')
    comedy_button = KeyboardButton('комедия')
    horrors_button = KeyboardButton('ужасы')
    crime_button = KeyboardButton('криминал')

    keyboard = ReplyKeyboardMarkup()
    keyboard.add(drama_button, action_button, comedy_button, horrors_button, crime_button)

    return keyboard