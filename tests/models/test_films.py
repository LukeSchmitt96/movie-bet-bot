from typing import Final
import unittest
from movie_bet_bot.models.movies import movies

film1: Final = movies.Film(title="film1", url="filmurl1")
film2: Final = movies.Film(title="film2", url="filmurl2")
film3: Final = movies.Film(title="film1", url="filmurl1")  # same as film1
film4 = movies.Film(title="film4", url="filmurl4")
film_dict: Final = {
    "title": film1.title,
    "url": film1.url,
    "runtime": film1.runtime,
    "poster_url": film1.poster_url,
    "timestamp": film1.timestamp,
}


class Test_Film(unittest.TestCase):
    def test_compare(self):
        self.assertNotEqual(film1, film2)
        self.assertEqual(film1, film3)

    def test_properties(self):
        rating = "★★★"
        self.assertEqual(film4.rating, "")
        film4.rating = rating
        self.assertEqual(film4.rating, rating)

    def test_to_dict(self):
        self.assertEqual(film1.to_dict(), film_dict)

    def test_repr(self):
        self.assertEqual(
            repr(film1),
            (
                f"Film(title='{film1.title}',url='{film1.url}',"
                f"runtime={film1.runtime},poster_url='{film1.poster_url}')"
            ),
        )
