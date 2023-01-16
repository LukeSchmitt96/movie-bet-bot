from movie_bet_bot.models.movies import Film

film1 = Film(title="film1", url="filmurl1")
film2 = Film(title="film2", url="filmurl2")
film3 = Film(title="film1", url="filmurl1")  # same as film1
film4 = Film(title="film4", url="filmurl4")


class Test_Film:
    def test_compare(self):
        assert film1 != film2
        assert film1 == film3
