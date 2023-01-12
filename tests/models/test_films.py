from movie_bet_bot.models.movies import Film, FilmList

from ..resources.test_list import PAGE

film1 = Film('film1', 'url1')
film2 = Film('film2', 'url2')
film3 = Film('film1', 'url1') # same as film1
film4 = Film('film4', 'url4')

class Test_Film:

    def test_compare(self):
        assert(film1 != film2)
        assert(film1 == film3)

class Test_FilmList:

    def test_compare(self):
        list1 = FilmList('url1', list([film1, film2]))
        list2 = FilmList('url2', list([film1, film2]))
        assert(list1 == list2)
        list2.films.append(film4)
        assert(list1 != list2)

    def test_from_html_string(self):
        flist = FilmList.from_html_string(PAGE)
        assert(len(flist) == 1)
        assert('Discord' in [f.title for f in flist])
