from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_answer() -> InlineKeyboardMarkup:
    yes_button = InlineKeyboardButton('Да', callback_data='yes')
    no_button = InlineKeyboardButton('Нет', callback_data='no')

    keyboard = InlineKeyboardMarkup()
    keyboard.add(yes_button, no_button)
    return keyboard


