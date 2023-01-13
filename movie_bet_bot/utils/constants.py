from typing import Dict

CONTEST_PLACE_MAP: Dict[int, str] = {
  1: "🥇",
  2: "🥈",
  3: "🥉",
}

LB_URL_ROOT = 'https://letterboxd.com'
POSTERPATH_URL_BASE = 'https://www.themoviedb.org/t/p/w92'

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

        span.name {
            display: inline-block;
            width: 60px;
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

        .film {
            margin-left: auto;
            margin-right: auto;
        }    </style>
</head>
"""

HTML_STANDINGS_TEMPLATE = """
<html>
    </head>
        {head}
    </head>
    <body>
        <p>Standings</p>
        <div class="members">
            {members}
        </div>
        <hr>
        <p>Since Last Update</p>
        <div class="films">
            {updates}
        </div>
    </body>
</html>
"""

HTML_STANDINGS_MEMBER = """
<div class="member">
    <span class="place">{place}</span>
    <span class="name">{name}:</span>
    <span class="score">{num_films_watched}</span>
    <span class="diff">+({films_since_last_update})</span>
</div>
"""

HTML_STANDINGS_UPDATE = """
<div class="watcher">
    <span class="name">{name}</span>
    {films}
</div>
"""

HTML_STANDINGS_UPDATE_FILMS = """
    <img class="film" src="{poster}" alt="">
"""
