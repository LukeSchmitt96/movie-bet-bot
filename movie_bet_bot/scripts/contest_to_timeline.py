from movie_bet_bot.models.movies.movies import Contest
from argparse import ArgumentParser
import yaml


class ContestToTimeline:
    def __init__(self, filepath_db: str, filepath_out: str) -> None:
        self.filepath_db = filepath_db
        with open(filepath_db) as conf_file:
            saved_data = yaml.safe_load(conf_file)
        contest = Contest.from_config(saved_data["contests"])[0]
        contest.to_timeline(filepath_out)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="ContestToTimeline",
        description="Convert a contest file and contest name to a timeline visualization.",
    )

    parser.add_argument("filepath_db")
    parser.add_argument("filepath_out")
    args = parser.parse_args()

    contest_to_timeline = ContestToTimeline(
        filepath_db=args.filepath_db,
        filepath_out=args.filepath_out,
    )
