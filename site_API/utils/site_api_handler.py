from typing import Dict
import requests


def _make_response(url: str, headers: Dict, success=200):
    response = requests.get(
        url,
        headers=headers
    )

    status_code = response.status_code

    if status_code == success:
        return response

    return status_code


def _get_movie(url: str, headers: Dict, movie_name: str, limit: int, func=_make_response):

    url = "{0}search?page=1&limit={1}&query={2}".format(url, limit, movie_name)
    response = func(url, headers=headers)
    return response


def _get_random_movie(url: str, headers: Dict, flag: str = None, released: int = None,
                      type_movie: str = None, genre: str = None, func=_make_response):

    if flag == 'no':
        url = "{0}random".format(url)
        response = func(url, headers=headers)
        return response
    else:
        url = "{0}random?notNullFields=name&".format(url)
        if isinstance(released, str):
            url += "year={0}&".format(released)
        if isinstance(type_movie, str):
            url += "type={0}&".format(type_movie)
        if isinstance(genre, str):
            url += "genre.name={0}".format(genre)
        response = func(url, headers=headers)
        return response


class SiteApiInterface():

    @staticmethod
    def get_movie():
        return _get_movie

    @staticmethod
    def get_random_movie():
        return _get_random_movie


if __name__ == "__main__":
    _make_response()
    _get_random_movie()
    _get_movie()

    SiteApiInterface()
