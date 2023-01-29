import unittest
from movie_bet_bot.utils import utils


class Test_Utils(unittest.TestCase):
    def test_map_place(self):
        self.assertEqual(utils.map_place(1), "🥇")
        self.assertEqual(utils.map_place(2), "🥈")
        self.assertEqual(utils.map_place(3), "🥉")
        self.assertEqual(utils.map_place(4), "4th")
