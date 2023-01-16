import copy

from movie_bet_bot.models.movies.movies import Film, Member

film1 = Film(title="film1", url="filmurl1")
film2 = Film(title="film2", url="filmurl2")
film3 = Film(title="film3", url="filmurl3")


class Test_Member:
    def test_compare(self):
        member1 = Member("member1", "contest_url1", "profile_url1")
        member1.list.url = "url1"
        member1.list.films.add((film1, film2))
        member1_updated = copy.deepcopy(member1)

        assert member1.list == member1_updated.list
        assert member1.num_films_watched == member1_updated.num_films_watched

        member1_updated.list.films.add(film3)
        assert member1.list != member1_updated.list
        assert member1.num_films_watched != member1_updated.num_films_watched
