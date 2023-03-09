from typing import Final
import unittest
from movie_bet_bot.models.movies import movies

from ..resources.test_list import PAGE

film1: Final = movies.Film(title="film1", url="filmurl1")
film2: Final = movies.Film(title="film2", url="filmurl2")
film3: Final = movies.Film(title="film1", url="filmurl1")  # same as film1
film4: Final = movies.Film(title="film4", url="filmurl4")
test_list: Final = movies.FilmList(url="url", films=list([film1, film2, film4]))
list_dict: Final = {
    "url": "url",
    "films": [
        film1.to_dict(),
        film2.to_dict(),
        film4.to_dict(),
    ],
}


class Test_FilmList(unittest.TestCase):
    def test_size(self):
        list1 = movies.FilmList(url="listurl1", films=list([film1, film2, film4]))
        list2 = movies.FilmList(url="listurl2", films=list([film1]))
        self.assertGreater(list1.films, list2.films)

    def test_compare(self):
        list1 = movies.FilmList(url="url1", films=set([film1, film2]))
        list2 = movies.FilmList(url="url1", films=set([film1, film2]))
        self.assertEqual(list1, list2)
        list2.films.add(film4)
        self.assertNotEqual(list1, list2)

    def test_from_html_string(self):
        flist = movies.FilmList.from_html_string(PAGE)
        self.assertEqual(len(flist), 1)
        self.assertIn("Discord", [f.title for f in flist.films])

    def test_subtract(self):
        list1 = movies.FilmList(url="listurl1", films=list([film1, film2, film4]))
        list2 = movies.FilmList(url="listurl2", films=list([film1]))
        self.assertEqual(set((list1 - list2)), set((film2, film4)))

    def test_film_titles(self):
        self.assertEqual(test_list.film_titles, ["film1", "film2", "film4"])

    def test_to_dict(self):
        self.assertEqual(test_list.to_dict(), list_dict)

    def test_repr(self):
        self.assertEqual(repr(test_list), f"FilmList(url={test_list.url},films={test_list.films})")
