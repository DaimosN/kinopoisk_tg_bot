from database.db_commands import SqlCommands
from loader import bot
from states.user_states import GetMovieByTitle
from telebot.types import Message
from site_API.core import headers, url, site_api
import json


@bot.message_handler(commands=['search_movie'])
def get_movie(message: Message) -> None:
    bot.set_state(message.from_user.id, GetMovieByTitle.movie_name, message.chat.id)
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.username} введи фильм для поиска")


@bot.message_handler(state=GetMovieByTitle.movie_name)
def get_count_for_search(message: Message) -> None:
    if message.text != '' and message.text is not None:
        bot.send_message(message.from_user.id, "Готово. Теперь введи какое максимальное количество совпадений вывести")
        bot.set_state(message.from_user.id, GetMovieByTitle.count_of_search)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["movie_name"] = message.text

    else:
        bot.send_message(message.from_user.id, "Необходимо ввести название фильма")


@bot.message_handler(state=GetMovieByTitle.count_of_search)
def get_count_for_search(message: Message):
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Готово. Осуществляю поиск")
        bot.set_state(message.from_user.id, GetMovieByTitle.count_of_search) # Нужно проверить кажется не нужно

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["count_of_search"] = message.text
        get_film = site_api.get_movie()
        response = get_film(url, headers, data["movie_name"], data["count_of_search"])
        insert_history = SqlCommands.insert()
        insert_history(
            message.from_user.id, message.from_user.username,
            command_name='search_with_name', movie_name=data["movie_name"]
        )
        if not isinstance(response, int):
            result = json.loads(response.text)
            for text in result["docs"]:
                report = f"Название фильма - {text['name']}\nГод выпуска - {text['year']}"
                bot.send_message(message.from_user.id, report)
                try:
                    bot.send_photo(message.from_user.id, photo=text['poster']['url'], caption=text['description'])
                except Exception:
                    report = f"остер отсутствует(\n{result['description']}"
                    bot.send_message(message.from_user.id, report)
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            bot.send_message(message.from_user.id, f"Возникла ошибка\n код ошибки {response}")
    else:
        bot.send_message(message.from_user.id, "Только цифры, пожалуйста")

    return data
