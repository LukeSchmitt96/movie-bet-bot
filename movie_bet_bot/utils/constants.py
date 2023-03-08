import os

import tmdbsimple as tmdb

tmdb.API_KEY = os.getenv("TMDB_API_KEY", default="")
TOKEN: str = os.getenv("DISCORD_TOKEN", default="")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", default=0))
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", default=0))
DB_PATH: str = os.getenv("DB_PATH", default="")

# Class name of the ul element containing the films in a Letterboxd List
LIST_CLASS_NAME = "poster-list"

# Class name of an li element containing a film in a Letterboxd List
FILM_CLASS_NAME = "film-detail"

# Class name of a span element containing the rating a member gave to a film in a Letterboxd List
FILM_RATING_CLASS_NAME = "rating"

# Letterboxd URL root
LB_URL_ROOT = "https://letterboxd.com"

# TMDB's URL base for its poster images. We are getting 92px width posters (w92)
POSTERPATH_URL_BASE = "https://www.themoviedb.org/t/p/w92"

# Base height of the image that will be created on updates. This number is the size of the
# member standings section in pixels
# IMAGE_BASE_HEIGHT = 218
IMAGE_BASE_HEIGHT = 200

# Head of the update image. Includes style
HTML_HEAD = """
<head>
    <style>
        * {
            font-size: large;
            font-weight: 700;
        }

        body {
            text-align: center;
            background-color: #23272A;
            color: #FFFFFF;
            font-family: Arial, Helvetica, sans-serif;
        }

        .members {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            height: min-content;
            width: fit-content;
            flex-direction: row;
            row-gap: 10px;
            grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        }

        .members>div.member {
            flex: 1 1 200px;
            height: min-content;
            margin: auto;
            align-items: center;
        }

        span.place {
            display: inline-block;
            width: 30px;
            text-align: center;
        }

        span.score {
            display: inline-block;
            width: 30px;
            text-align: center;
        }

        span.diff {
            display: inline-block;
            width: 30px;
            text-align: center;
        }

        span.name {
            display: inline-block;
            width: 60px;
            text-align: center;
        }

        span.hours {
            display: inline-block;
            text-align: center;
        }

        .films {
            display: flex;
            height: fit-content;
            flex-direction: column;
        }

        .films>.watcher {
            display: flex;
            flex-wrap: nowrap;
            flex-direction: row;
            flex: 1 1 150px;
            height: fit-content;
            align-items: center;
            margin: 0 100px;
        }

        .watcher>.name {
            position: absolute;
            margin: -100px;
        }

        .watcher>.film-container {
            width: 100%;
            display: flex;
            flex-direction: column;
        }

        .film-container>.film-poster {
            margin-left: auto;
            margin-right: auto;
        }

        .film-container>.film-rating {
            margin-left: auto;
            margin-right: auto;
            color: #00C030;
            height: 2em;
        }

        .hidden {
            display: none !important;
        }
    </style>
</head>
"""

# Template for the update image
HTML_STANDINGS_TEMPLATE = """
<html>
    </head>
        {head}
    </head>
    <body>
        <p>Standings as of {time}</p>
        <div class="members">
            {members}
        </div>
        <hr>
        <p class="{updates_head_class}">{updates_head}</p>
        <div class="{updates_class}">
            {updates}
        </div>
    </body>
</html>
"""

# Template for each member in the standings update image
HTML_STANDINGS_MEMBER = """
<div class="member">
    <span class="place">{place}</span>
    <span class="name">{name}:</span>
    <span class="score">{num_films_watched}</span>
    <span class="hours {hours_class}">{hours_watched}</span>
    <span class="diff">{films_since_last_update}</span>
</div>
"""

# Template for a member's new films watched in the standings update image
HTML_STANDINGS_UPDATE = """
<div class="watcher">
    <span class="name">{name}</span>
    {films}
</div>
"""

# Template for each new film watched by a member in the standings update image
HTML_STANDINGS_UPDATE_FILMS = """
<div class="film-container">
    <img class="film-poster" src="{poster}" alt="">
    <span class="film-rating">{rating}</span>
</div>
"""
