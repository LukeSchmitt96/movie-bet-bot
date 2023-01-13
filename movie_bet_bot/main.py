import os
from typing import Dict

import tmdbsimple as tmdb
import yaml
from dotenv import load_dotenv

from movie_bet_bot.models.bot import MovieBetBot
from movie_bet_bot.models.movies import Contest

load_dotenv()
tmdb.API_KEY = os.getenv('TMDB_API_KEY')
conf: Dict = None


def main():
    print('Opening db file...')
    with open(os.getenv('DB_PATH')) as conf_file:
        print('Opened db!')
        saved_data = yaml.safe_load(conf_file)
        bot = MovieBetBot(
            contest=Contest.from_config(saved_data['contests'])[0]
        )
    bot.run()


if __name__ == '__main__':
    main()
