def map_place(place: int) -> str:
    match place:
        case 1:
            return "🥇"
        case 2:
            return "🥈"
        case 3:
            return "🥉"
        case _:
            return f"{place}th"
