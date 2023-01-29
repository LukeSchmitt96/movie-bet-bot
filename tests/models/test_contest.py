import copy
import os
from typing import Final
import unittest

import yaml

from movie_bet_bot.models.movies import movies

member1 = movies.Member(
    "name1",
    "https://letterboxd.com/moviebetbot/list/test_list_1/detail/",
    "profile_url1",
)
member2 = movies.Member(
    "name2",
    "https://letterboxd.com/moviebetbot/list/test_list_2/detail/",
    "profile_url2",
)

test_c = movies.Contest(
    name="test",
    members=[member1, member2],
)

contest_dict: Final = {
    "name": test_c.name,
    "members": [member.to_dict() for member in test_c.members],
}


class Test_Contest(unittest.TestCase):
    def test_from_config(self):
        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "resources", "test_config.yaml"
            )
        ) as test_conf:
            saved_data = yaml.safe_load(test_conf)
        movies.Contest.from_config(saved_data.get("contests"))[0]


class Test_Contest_AsyncIO(unittest.IsolatedAsyncioTestCase):
    async def test_run_contest(self):
        c = copy.deepcopy(test_c)
        assert c.members[0].name == "name1"
        assert c.members[1].name == "name2"
        await c.update(get_film_details=False, save_on_update=False)
        assert c.members[0].name == "name2"
        assert c.members[0].num_films_watched == 2
        assert c.members[1].name == "name1"
        assert c.members[1].num_films_watched == 1
