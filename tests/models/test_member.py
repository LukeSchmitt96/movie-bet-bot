import copy
from typing import Final

from movie_bet_bot.models.movies.movies import Film, Member

film1: Final = Film(title="film1", url="filmurl1")
film2: Final = Film(title="film2", url="filmurl2")
film3: Final = Film(title="film3", url="filmurl3")

test_member = Member("member1", "contest_url1", "profile_url1")
test_member.list.url = "url1"
test_member.list.films.update([film1, film2])
member_dict: Final = {
    "contest_url": test_member.contest_url,
    "profile_url": test_member.profile_url,
    "name": test_member.name,
    "list": test_member.list.to_dict(),
    "watchtime": test_member.watchtime,
    "films_since_last_update": test_member.num_films_since_last_update,
}


class Test_Member:
    def test_compare(self):
        member = copy.deepcopy(test_member)
        member_updated = copy.deepcopy(test_member)

        assert member.list == member_updated.list
        assert member.num_films_watched == member_updated.num_films_watched

        member_updated.list.films.update([film3])
        assert member.list != member_updated.list
        assert member.num_films_watched != member_updated.num_films_watched

    def test_to_dict(self):
        assert test_member.to_dict() == member_dict

    def test_repr(self):
        assert repr(test_member) == (
            f"Member(name={test_member.name},list={test_member.list})"
        )
