def map_place(place: int) -> str:
    """
    Map place to corresponding emoji or ordinal number.

    :param place: place to map
    :return: emoji or ordinal number representing place in standings
    """
    match place:
        case 1:
            return "🥇"
        case 2:
            return "🥈"
        case 3:
            return "🥉"
        case _:
            return f"{place}th"
