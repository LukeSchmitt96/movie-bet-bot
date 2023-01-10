from typing import Dict

import yaml
from dotenv import load_dotenv

from movie_bet_bot.models.bot import MovieBetBot
from movie_bet_bot.models.movies import Contest
from movie_bet_bot.utils import parse_config

load_dotenv()
conf: Dict = None

def main():
    with open('./movie_bot_conf.yaml') as conf_file:
        conf = parse_config(yaml.safe_load(conf_file))
    bot = MovieBetBot(
        contest=Contest.from_config(conf['contest_config'])[0]
    )
    bot.run()

if __name__ == '__main__':
    main()
