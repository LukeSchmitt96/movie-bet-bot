import pytest

from movie_bet_bot.models.movies.movies import Contest, Member


class Test_Contest:
    @pytest.mark.asyncio
    async def test_run_contest(self):
        c = Contest(
            name="test",
            members=[
                Member(
                    "name1",
                    "https://letterboxd.com/moviebetbot/list/test_list_1/detail/",
                    "profile_url1",
                ),
                Member(
                    "name2",
                    "https://letterboxd.com/moviebetbot/list/test_list_2/detail/",
                    "profile_url2",
                ),
            ],
        )
        assert c.members[0].name == "name1"
        assert c.members[1].name == "name2"
        await c.update(get_film_details=False, save_on_update=False)
        assert c.members[0].name == "name2"
        assert c.members[0].num_films_watched == 2
        assert c.members[1].name == "name1"
        assert c.members[1].num_films_watched == 1
