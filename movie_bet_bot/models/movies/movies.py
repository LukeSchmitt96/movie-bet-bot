from __future__ import annotations
import copy

from datetime import datetime
from typing import List, Set

from bs4 import BeautifulSoup

from movie_bet_bot.utils import fetch_page_body_from_url, map_place
from movie_bet_bot.utils.constants import LB_ROOT

LIST_CLASS_NAME = 'poster-list'
FILM_CLASS_NAME = 'film-detail'


class Film:
    title: str
    url: str
    runtime: int
    poster_url: str

    def __init__(self, title: str, url: str) -> None:
        self.title = title
        self.url = url

    def __repr__(self) -> str:
        return f"Film(title='{self.title}',url='{self.url}')"

    def __eq__(self, __o: Film) -> bool:
        return self.title == __o.title and self.url == __o.url

    def __hash__(self):
        return hash(tuple((self.title, self.url)))


class FilmList:
    url: str
    films: Set[Film]

    def __init__(self, url: str, films: Set[Film] = set()) -> None:
        self.url = url
        self.films = films

    @staticmethod
    async def from_url(url: str) -> Set[Film]:
        films: Set[Film] = set()
        page = await fetch_page_body_from_url(url)
        list_result = page.find_all('li', class_=FILM_CLASS_NAME)
        for li in list_result:
            films.add(Film(li.a.text, LB_ROOT + li.a['href']))
        return films

    @staticmethod
    def from_html_string(html: str) -> Set[Film]:
        html_soup = BeautifulSoup(html, 'html.parser')
        films: Set[Film] = set()
        list_result = html_soup.find_all('li', class_=FILM_CLASS_NAME)
        for li in list_result:
            films.add(Film(li.a.text, LB_ROOT + li.a['href']))
        return films

    def __repr__(self) -> str:
        return f'Film(url={self.url},films={self.films})'

    def __len__(self) -> int:
        return len(self.films)

    def __hash__(self) -> int:
        return hash(self.films)

    def __eq__(self, __o: FilmList) -> bool:
        return self.url == __o.url and self.films == __o.films

    def __sub__(self, __o: FilmList) -> List[Film]:
        diff = set([(f.title, f.url) for f in self.films]) - set([(f.title, f.url) for f in __o.films])
        return [Film(f[0], f[1]) for f in diff]


class Member:
    contest_url: str
    profile_url: str
    name: str
    list: FilmList = FilmList('')
    watchtime: int

    def __init__(self, name: str, contest_url: str, profile_url: str) -> None:
        self.name = name
        self.contest_url = contest_url
        self.profile_url = profile_url

    def num_films_watched(self) -> int:
        return len(self.list)

    def __repr__(self) -> str:
        return f"Member(name={self.name},list={self.list})"

    def __hash__(self) -> int:
        return hash((self.profile_url, self.list))


class Contest:
    name: str
    members: List[Member]

    def __init__(self, name, members: List[Member]) -> None:
        self.name = name
        self.members = members

    def from_config(config: dict) -> List[Contest]:
        contests = []
        for contest_conf in config:
            members = []
            for member_conf in contest_conf['members']:
                members.append(
                    Member(
                        name=member_conf['name'],
                        profile_url=member_conf['profile_url'],
                        contest_url=member_conf['contest_url'],
                    )
                )
            contests.append(
                Contest(
                    name=contest_conf['name'],
                    members=members,
                )
            )
        return contests

    async def update(self) -> bool:
        is_changed = False
        for member in self.members:
            member_last = copy.deepcopy(member)
            member.list = await FilmList.from_url(member_last.contest_url)
            if member == member_last:
                is_changed = True
        self.members.sort(
            key=lambda x: x.num_films_watched(),
            reverse=True
        )
        return is_changed

    def print_standings(self) -> str:
        now = datetime.now()
        dt_string = now.strftime("%m/%d %H:%M")
        out_string = f'Standings as of {dt_string}:\n'
        place = 1
        last_member_films_watched = -1
        for member in self.members:
            if (member.num_films_watched() < last_member_films_watched):
                place += 1
            last_member_films_watched = member.num_films_watched()
            out_string += (
                f'* {map_place(place)} '
                f'{member.name}: '
                f'{member.num_films_watched()}'
                '\n'
            )
        print(out_string)
        return out_string
