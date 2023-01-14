# Movie Bet Bot [![CI](https://github.com/LukeSchmitt96/movie-bet-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/LukeSchmitt96/movie-bet-bot/actions/workflows/ci.yml)

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
$ poetry install --with test
```

4. Configure project's `<project_root>/movie_bot_conf.yaml` file

```yaml
contests:
  - name: NAME
    members:
    - name: NAME_1
      profile_url: PROFILE_URL_1
      contest_url: CONTEST_URL_1
    - name: NAME_2
      profile_url: PROFILE_URL_2
      contest_url: CONTEST_URL_2
bot:
  interval_callback_duration: 120000
```

5. Configure project's `<project_root>/.env` file

```bash
DISCORD_TOKEN="..."
DISCORD_GUILD_ID="..."
DISCORD_CHANNEL_ID="..."
```

6. (Optional) Run tests

```console
$ poetry run pytest
```

7. Run project

```console
$ poetry run python ./movie_bet_bot/main.py
```
