from movie_bet_bot.utils.constants import CONTEST_PLACE_MAP

def map_place(place: int) -> str:
    if place in CONTEST_PLACE_MAP.keys():
        return CONTEST_PLACE_MAP.get(place)
    else:
        return f'{place}th'
