from movie_bet_bot.utils import map_place


class Test_Utils:
    def test_map_place(self):
        assert map_place(1) == "🥇"
        assert map_place(2) == "🥈"
        assert map_place(3) == "🥉"
        assert map_place(4) == "4th"
