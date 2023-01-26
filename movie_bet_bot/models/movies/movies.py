from __future__ import annotations
import copy

from datetime import datetime
from typing import Dict, List, Set, Union
import yaml
import tmdbsimple as tmdb

from bs4 import BeautifulSoup

from movie_bet_bot.utils import constants, fetch_page_body_from_url, map_place
from movie_bet_bot.utils.images import html_to_image


class Film:
    title: str
    url: str
    runtime: int = -1
    poster_url: str = ""
    _rating: str = ""

    def __init__(
        self,
        title: str,
        url: str,
        runtime: int = -1,
        poster_url: str = "",
    ) -> None:
        self.title = title
        self.url = url
        self.runtime = runtime
        self.poster_url = poster_url

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "url": self.url,
            "runtime": self.runtime,
            "poster_url": self.poster_url,
        }

    @property
    def rating(self) -> str:
        return self._rating

    @rating.setter
    def rating(self, r) -> None:
        self._rating = r

    def __repr__(self) -> str:
        return (
            f"Film(title='{self.title}',url='{self.url}',"
            f"runtime={self.runtime},poster_url='{self.poster_url}')"
        )

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
    async def from_url(url: str, get_film_details: bool = True) -> FilmList:
        films: Set[Film] = set()
        list_page = await fetch_page_body_from_url(url)
        list_result = list_page.find_all("li", class_=constants.FILM_CLASS_NAME)
        li: BeautifulSoup
        for li in list_result:
            film_title = li.a.text
            film_year = li.find_all("small", {"class": "metadata"})[0].a.text.strip()
            film_url = constants.LB_URL_ROOT + li.a["href"]
            film = Film(film_title, film_url)
            try:
                film.rating = li.find_all("span", {"class": "rating"})[0].text.strip()
            except (AttributeError, IndexError):
                pass
            if get_film_details:
                search = tmdb.Search()
                resp = search.movie(query=film_title, year=film_year)
                if "results" in resp:
                    film_info = tmdb.Movies(int(resp["results"][0]["id"])).info()
                    film.poster_url = (
                        constants.POSTERPATH_URL_BASE + film_info["poster_path"]
                    )
                    film.runtime = int(film_info["runtime"])
            films.add(film)
        return FilmList(url, films)

    @property
    def film_titles(self) -> List[str]:
        return [film.title for film in self.films]

    @staticmethod
    def from_html_string(html: str) -> FilmList:
        html_soup = BeautifulSoup(html, "html.parser")
        films: Set[Film] = set()
        list_result = html_soup.find_all("li", class_=constants.FILM_CLASS_NAME)
        for li in list_result:
            films.add(Film(li.a.text, constants.LB_URL_ROOT + li.a["href"]))
        return FilmList("", films)

    def to_dict(self) -> Dict[str, Union[str, List[Dict]]]:
        return {
            "url": self.url,
            "films": [film.to_dict() for film in self.films],
        }

    def __repr__(self) -> str:
        return f"Film(url={self.url},films={self.films})"

    def __len__(self) -> int:
        return len(self.films)

    def __hash__(self) -> int:
        return hash(self.films)

    def __eq__(self, __o: FilmList) -> bool:
        return self.url == __o.url and self.films == __o.films

    def __sub__(self, __o: FilmList) -> List[Film]:
        diff = set([(f.title, f.url) for f in self.films]) - set(
            [(f.title, f.url) for f in __o.films]
        )
        return [Film(f[0], f[1]) for f in diff]


class Member:
    contest_url: str
    profile_url: str
    name: str
    list: FilmList = FilmList("")
    _watchtime: int = -1
    _num_films_since_last_update: int = 0
    _films_since_last_update: Set[Film] = []
    _place: int = -1

    def __init__(
        self,
        name: str,
        contest_url: str,
        profile_url: str,
        list: FilmList = FilmList(""),
    ) -> None:
        self.name = name
        self.contest_url = contest_url
        self.profile_url = profile_url
        self.list = list

    @property
    def place(self) -> int:
        return self._place

    @place.setter
    def place(self, value):
        self._place = value

    @property
    def num_films_watched(self) -> int:
        return len(self.list)

    @property
    def watchtime(self) -> int:
        return sum([film.runtime for film in self.list.films])

    @property
    def num_films_since_last_update(self) -> int:
        return self._num_films_since_last_update

    @num_films_since_last_update.setter
    def num_films_since_last_update(self, num):
        self._num_films_since_last_update = num

    def films_in_update(self, update: Set[Film]):
        self._films_since_last_update = self.list.films - update
        return self._films_since_last_update

    def to_dict(self) -> Dict[str, Union[str, int, Dict]]:
        return {
            "contest_url": self.contest_url,
            "profile_url": self.profile_url,
            "name": self.name,
            "list": self.list.to_dict(),
            "watchtime": self.watchtime,
            "films_since_last_update": self.num_films_since_last_update,
        }

    def __repr__(self) -> str:
        return f"Member(name={self.name},list=[{self.list}])"

    def __hash__(self) -> int:
        return hash((self.profile_url, self.list))


class Contest:
    name: str
    members: List[Member]
    standings_string: str = ""

    def __init__(
        self,
        name,
        members: List[Member] = [],
    ) -> None:
        self.name = name
        self.members = members

    @staticmethod
    def from_config(config: dict) -> List[Contest]:
        contests: List[Contest] = []
        for contest_conf in config:
            members: List[Member] = []
            for member_conf in contest_conf["members"]:
                member = Member(
                    name=member_conf["name"],
                    profile_url=member_conf["profile_url"],
                    contest_url=member_conf["contest_url"],
                    list=FilmList(
                        url=member_conf["contest_url"],
                        films=set(
                            [
                                Film(
                                    title=film["title"],
                                    url=film["url"],
                                    runtime=film["runtime"],
                                    poster_url=film["poster_url"],
                                )
                                for film in member_conf["list"]["films"]
                            ]
                        ),
                    ),
                )
                members.append(member)
            contests.append(
                Contest(
                    name=contest_conf["name"],
                    members=members,
                )
            )
        return contests

    async def update(
        self, get_film_details: bool = True, save_on_update: bool = True
    ) -> bool:
        print("Updating...")
        is_changed = False
        for member in self.members:
            member_last = copy.deepcopy(member)
            member.list = await FilmList.from_url(
                url=member_last.contest_url,
                get_film_details=get_film_details,
            )
            if member.list != member_last.list:
                is_changed = True
                member.num_films_since_last_update = len(member.list) - len(
                    member_last.list
                )
                member.films_in_update(member_last.list.films)
            else:
                member.num_films_since_last_update = 0

        # sort members by number of films watched first and watchtime second
        self.members.sort(
            key=lambda x: (x.num_films_watched, x.watchtime), reverse=True
        )

        if save_on_update and is_changed:
            self.save()
        else:
            print("No change since last update.")

        self.update_standings()
        return is_changed

    def update_standings(self) -> None:
        self.time_last_update = datetime.now()
        self.standings_string = (
            f'Standings as of {self.time_last_update.strftime("%m/%d %H:%M")}:\n'
        )
        place = 1
        for member in self.members:
            member.place = place
            place += 1
            self.standings_string += (
                f"* {map_place(member.place)}\t"
                f"{member.name}:\t"
                f"{member.num_films_watched}\t"
                f"(+{member.num_films_since_last_update})\t"
                f"{member.watchtime / 60:.1f}hrs"
                "\n"
            )
        print(self.standings_string)

    def to_dict(self) -> Dict[str, Union[str, List[Dict]]]:
        return {
            "name": self.name,
            "members": [member.to_dict() for member in self.members],
        }

    def load(self) -> None:
        print(f"Attempting to load from database at '{constants.DB_PATH}'...")
        try:
            with open(constants.DB_PATH, "r") as db_file:
                saved_data = yaml.safe_load(db_file)
                if saved_data is None:
                    return
                conf = Contest.from_config(saved_data["contests"], from_config=False)[0]
                self.members = conf.members
            print("Loaded!")
        except OSError as e:
            print(f"Problem with database file at '{constants.DB_PATH}': ", e)

    def save(self) -> None:
        print(f"Attempting to save to database at '{constants.DB_PATH}'...")
        try:
            with open(constants.DB_PATH, "w") as db_file:
                db_file.write(
                    yaml.safe_dump(
                        {
                            "contests": [self.to_dict()],
                        }
                    )
                )
            print("Saved!")
        except OSError as e:
            print(f"Problem with database file at '{constants.DB_PATH}': ", e)

    def to_image(self) -> List[str]:
        html_height = constants.IMAGE_BASE_HEIGHT  # height of created image
        html_members = (
            ""  # html str w/ current scores, num of films watched since last update
        )
        html_updates = ""  # html str w/ all member's films watched since last update
        for member in self.members:
            html_films = ""  # html str w/ a member's films watched since last update
            html_films_since_last_update = (
                f"(+{member.num_films_since_last_update})"
                if member.num_films_since_last_update > 0
                else ""
            )
            html_members += constants.HTML_STANDINGS_MEMBER.format(
                place=map_place(member.place),
                name=member.name,
                num_films_watched=member.num_films_watched,
                films_since_last_update=html_films_since_last_update,
            )
            # skip adding member to update if no films in this update
            if member.num_films_since_last_update < 1:
                continue
            for film in member._films_since_last_update:
                html_films += constants.HTML_STANDINGS_UPDATE_FILMS.format(
                    poster=film.poster_url,
                    rating=film.rating,
                )
            html_updates += constants.HTML_STANDINGS_UPDATE.format(
                name=member.name, films=html_films
            )
            html_height += 174
        return html_to_image(
            html=constants.HTML_STANDINGS_TEMPLATE.format(
                head=constants.HTML_HEAD,
                time=self.time_last_update.strftime("%m/%d %H:%M"),
                members=html_members,
                updates=html_updates,
            ),
            out="update_image.png",
            size=(480, html_height + 20),
        )
