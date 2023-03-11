import copy
import os
from typing import Final
import unittest
from bs4 import BeautifulSoup

import yaml

from movie_bet_bot.models.movies import movies


unittest.TestLoader.sortTestMethodsUsing = None

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
            os.path.join(os.path.dirname(__file__), "..", "resources", "test_config.yaml")
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
        assert c.members[0].num_films_since_last_update == 2
        assert c.members[1].name == "name1"
        assert c.members[1].num_films_watched == 1
        assert c.members[1].num_films_since_last_update == 1
        test_html, _ = c.to_image_html()
        test_soup = BeautifulSoup(test_html, "html.parser")
        diff_spans = test_soup.find_all("span", {"class": "diff"})
        assert "(+2)" in diff_spans[0]
        assert "(+1)" in diff_spans[1]
        member_div_soup = test_soup.find("div", {"class": "members"})
        member_name_spans = member_div_soup.find_all("span", {"class": "name"})
        assert "name2:" in member_name_spans[0]
        assert "name1:" in member_name_spans[1]
