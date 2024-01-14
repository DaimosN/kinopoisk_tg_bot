from loader import bot
from states.user_states import GetRandomMovieWithParams
from telebot.types import Message
from site_API.core import headers, url, site_api
import json
from keyboards.reply import default_button as reply_button
from keyboards.inline import default_button
from database.db_commands import SqlCommands


@bot.message_handler(commands=['search_random_movie'])
def get_movie(message: Message) -> None:
    keyboards = default_button.get_answer()
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.username} хочешь указать параметры для поиска?\n"
                                           f"Выберите 'Да' или 'Нет'",
                     reply_markup=keyboards)


@bot.callback_query_handler(func=lambda message: message.data == 'no' and 'параметры для' in message.message.text)
def callback_query(message):
    bot.send_message(message.from_user.id, "Начинаю поиск")
    get_random_film = site_api.get_random_movie()
    insert_history = SqlCommands.insert()
    insert_history(
        message.from_user.id, message.from_user.username,
        command_name='random_search_without_params'
    )
    response = get_random_film(url, headers, message.data)
    if not isinstance(response, int):
        result = json.loads(response.text)

        report = f"Название фильма - {result['name']}\nГод выпуска - {result['year']}\n" \
                 f"Описание: {result['description']}"
        bot.send_message(message.from_user.id, report.replace("None", "Неизвестно"))
        try:
            bot.send_photo(message.from_user.id, photo=result['poster']['url'], caption=result['description'])
        except Exception:
            report = f"остер отсутствует(\n{result['description']}"
            bot.send_message(message.from_user.id, report)
    else:
        bot.send_message(message.from_user.id, f"Возникла ошибка\n код ошибки {response}")


@bot.callback_query_handler(func=lambda message: message.data == 'yes' and 'параметры для' in message.message.text)
def callback_query(message):
    bot.set_state(message.from_user.id, GetRandomMovieWithParams.released, message.message.chat.id)
    bot.send_message(message.from_user.id, f"{message.from_user.username} введи год выхода фильма")


@bot.message_handler(state=GetRandomMovieWithParams.released)
def get_type_movie_for_search(message: Message) -> None:
    if message.text.isdigit():
        keyboards = reply_button.get_type_movie()
        bot.send_message(message.from_user.id, "Готово. Теперь выберите какой тип искать", reply_markup=keyboards)
        bot.set_state(message.from_user.id, GetRandomMovieWithParams.type)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["released"] = message.text
    else:
        bot.send_message(message.from_user.id, "Необходимо указать год в цифровом виде")


@bot.message_handler(state=GetRandomMovieWithParams.type)
def get_genre_for_search(message: Message) -> None:
    if message.text.isalpha():
        keyboards = reply_button.get_genres_movie()
        bot.send_message(message.from_user.id, "Готово. Теперь выберите какой жанр искать", reply_markup=keyboards)
        bot.set_state(message.from_user.id, GetRandomMovieWithParams.genre)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["type"] = message.text
    else:
        bot.send_message(message.from_user.id, "Необходимо выбрать жанр фильма")


@bot.message_handler(state=GetRandomMovieWithParams.genre)
def get_request(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, "Готово. Осуществляю поиск по вашим критериям")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["genre"] = message.text
        get_random_film = site_api.get_random_movie()
        response = get_random_film(url, headers, released=data["released"], type_movie=data["type"],
                                   genre=data["genre"])
        insert_history = SqlCommands.insert()
        insert_history(
            message.from_user.id, message.from_user.username,
            command_name='random_search_with_params', released=data["released"],
            movie_type=data["type"], movie_genre=data["genre"]
        )
        if not isinstance(response, int):
            result = json.loads(response.text)

            report = f"Название фильма - {result['name']}\nГод выпуска - {result['year']}"
            bot.send_message(message.from_user.id, report)
            try:
                bot.send_photo(message.from_user.id, photo=result['poster']['url'], caption=result['description'])
            except Exception:
                report = f"остер отсутствует(\n{result['description']}"
                bot.send_message(message.from_user.id, report)

            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id, f"Возникла ошибка\n код ошибки {response}")



