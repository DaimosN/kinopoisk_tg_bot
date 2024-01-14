from loader import bot
from telebot.types import Message
from keyboards.inline import default_button
from database.db_commands import SqlCommands
from states.user_states import GetDigitForSearch


@bot.message_handler(commands=['history'])
def get_history(message: Message) -> None:
    keyboards = default_button.get_answer()
    bot.send_message(message.from_user.id,
                     f"Привет, {message.from_user.username} хочешь указать количество строк, которые нужно вернуть?\n"
                     f"Выберите 'Да' или 'Нет'",
                     reply_markup=keyboards)


@bot.callback_query_handler(func=lambda message: message.data == 'no' and 'количество строк' in message.message.text)
def callback_query_no(message):
    bot.send_message(message.from_user.id, "Загружаю всю историю запросов")
    select_history = SqlCommands.select()
    result = select_history(message.data, message.from_user.id)
    return_history(result, message)


@bot.callback_query_handler(func=lambda message: message.data == 'yes' and 'количество строк' in message.message.text)
def callback_query_yes(message):
    bot.set_state(message.from_user.id, GetDigitForSearch.digit_of_search, message.message.chat.id)
    bot.send_message(message.from_user.id, "Укажите какое количество запросов вернуть")


@bot.message_handler(state=GetDigitForSearch.digit_of_search)
def get_history_with_params(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Готово. Начинаю поиск")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["released"] = message.text
        select_history = SqlCommands.select()
        result = select_history("yes", message.from_user.id, data["released"])
        bot.delete_state(message.from_user.id, message.chat.id)
        return_history(result, message)
    else:
        bot.send_message(message.from_user.id, "Необходимо указать количество в цифровом виде")


def return_history(result: list, message: Message) -> None:
    if len(result) != 0:
        for res in result:
            report = f"Вы искали:\n"\
                     f"Название команды - {res.command_name}\n"\
                     f"Название фильма - {res.movie_name}\n"\
                     f"Год выхода фильма - {res.released}\n"\
                     f"Категория произведения - {res.movie_type}\n"\
                     f"Жанр - {res.movie_genre}"
            bot.send_message(message.from_user.id,
                             report.replace("None", "Отсутствует")
                             )
    else:
        bot.send_message(message.from_user.id,
                         f"Возможно история недоступна, либо вы ещё ничего не искали)")
