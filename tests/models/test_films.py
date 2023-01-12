import copy

import pytest

from movie_bet_bot.models.movies import Contest, Film, FilmList, Member

from ..resources.test_list import PAGE

film1 = Film(title='film1', url='filmurl1')
film2 = Film(title='film2', url='filmurl2')
film3 = Film(title='film1', url='filmurl1') # same as film1
film4 = Film(title='film4', url='filmurl4')

class Test_Film:

    def test_compare(self):
        assert(film1 != film2)
        assert(film1 == film3)

class Test_FilmList:

    def test_compare(self):
        list1 = FilmList(
            url='url1',
            films=set([film1, film2])
        )
        list2 = FilmList(
            url='url1',
            films=set([film1, film2])
        )
        assert(list1 == list2)
        list2.films.add(film4)
        assert(list1 != list2)

    def test_from_html_string(self):
        flist = FilmList.from_html_string(PAGE)
        assert(len(flist) == 1)
        assert('Discord' in [f.title for f in flist])

    def test_subtract(self):
        list1 = FilmList(
            url='listurl1',
            films=list([film1, film2, film4])
        )
        list2 = FilmList(
            url='listurl2',
            films=list([film1])
        )
        assert(set((list1 - list2)) == set((film2, film4)))

    def test_size(self):
        list1 = FilmList(
            url='listurl1',
            films=list([film1, film2, film4])
        )
        list2 = FilmList(
            url='listurl2',
            films=list([film1])
        )
        assert(list1.films > list2.films)


class Test_Member:

    def test_compare(self):
        member1 = Member('member1', 'contest_url1', 'profile_url1')
        member1.list.url='url1'
        member1.list.films.add((film1, film2))
        member1_updated = copy.deepcopy(member1)
        assert(member1.list == member1_updated.list)
        member1_updated.list.films.add(film4)
        assert(member1.list == member1_updated.list)


class Test_Contest:

    @pytest.mark.asyncio
    async def test_run_contest(self):
        c = Contest(
            name='test',
            members=[
                Member(
                    'name1',
                    'https://letterboxd.com/moviebetbot/list/test_list_1/detail/',
                    'profile_url1'
                ),
                Member(
                    'name2',
                    'https://letterboxd.com/moviebetbot/list/test_list_2/detail/',
                    'profile_url2'
                ),
            ]
        )
        assert(c.members[0].name == 'name1')
        assert(c.members[1].name == 'name2')
        await c.run_contest()
        assert(c.members[0].name == 'name2')
        assert(c.members[0].get_number_of_films_watched() == 2)
        assert(c.members[1].name == 'name1')
        assert(c.members[1].get_number_of_films_watched() == 1)
