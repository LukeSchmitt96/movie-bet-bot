import unittest

from movie_bet_bot.utils import fetchers


class Test_Fetch_Page_Body_URL(unittest.IsolatedAsyncioTestCase):
    async def test_invalid_url(self):
        empty = await fetchers.fetch_page_body_from_url("https://invalid.example.com/")
        self.assertEqual(empty, "")
