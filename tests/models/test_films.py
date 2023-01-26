from typing import Final
from movie_bet_bot.models.movies import Film

film1: Final = Film(title="film1", url="filmurl1")
film2: Final = Film(title="film2", url="filmurl2")
film3: Final = Film(title="film1", url="filmurl1")  # same as film1
film4 = Film(title="film4", url="filmurl4")
film_dict: Final = {
    "title": film1.title,
    "url": film1.url,
    "runtime": film1.runtime,
    "poster_url": film1.poster_url,
}


class Test_Film:
    def test_compare(self):
        assert film1 != film2
        assert film1 == film3

    def test_properties(self):
        rating = "★★★"
        assert film4.rating == ""
        film4.rating = rating
        assert film4.rating == rating

    def test_to_dict(self):
        assert film1.to_dict() == film_dict

    def test_repr(self):
        assert repr(film1) == (
            f"Film(title='{film1.title}',url='{film1.url}',"
            f"runtime={film1.runtime},poster_url='{film1.poster_url}')"
        )
