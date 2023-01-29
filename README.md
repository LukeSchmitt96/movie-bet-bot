# Movie Bet Bot

## CI Status
[![CI](https://github.com/LukeSchmitt96/movie-bet-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/LukeSchmitt96/movie-bet-bot/actions/workflows/ci.yml) [![pre-commit](https://github.com/LukeSchmitt96/movie-bet-bot/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/LukeSchmitt96/movie-bet-bot/actions/workflows/pre-commit.yml) ![Coverage](images/coverage.svg)

## Installation

1. Install [Poetry](https://python-poetry.org/docs/)

```console
$ curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone repo

```console
$ git clone https://github.com/LukeSchmitt96/movie-bet-bot.git
```

3. Install project with Poetry

```console
$ poetry install --with test,dev
```

4. Seed bot's database

```yaml
contests:
- members:
  - contest_url: https://letterboxd.com/PROFILE/list/LIST_NAME/detail/
    list:
      films: []
      url: https://letterboxd.com/PROFILE/list/LIST_NAME/detail/
    name: NAME
    profile_url: https://letterboxd.com/PROFILE/
    watchtime: 0
  - contest_url: https://letterboxd.com/NAME/list/LIST_NAME/detail/
    list:
      films: []
      url: https://letterboxd.com/PROFILE/list/LIST_NAME/detail/
    name: NAME
    profile_url: https://letterboxd.com/PROFILE/
    watchtime: 0

  ...

  name: CONTEST_NAME
```

5. Configure bot's `<project_root>/.env` file

```bash
DISCORD_TOKEN="..."
DISCORD_GUILD_ID="..."
DISCORD_CHANNEL_ID="..."
TMDB_API_KEY="..."
DB_PATH="..."
```

6. (Optional) Run tests, pre-commit hooks

```console
$ poetry run task test
$ poetry run task pre-commit
```

7. Run bot

```console
$ poetry run task start
```
