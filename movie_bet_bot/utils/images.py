from typing import Tuple

from html2image import Html2Image

from movie_bet_bot.utils import constants
from movie_bet_bot.utils.utils import map_place

FLAGS = [
    "--default-background-color=000000",
    "--hide-scrollbars",
]


def html_to_image(html: str, out: str = None, size: Tuple[int] = (480, 800)) -> str:
    """
    Create image from html.

    :param html: HTML to render as an image
    :param out: save location of image
    :param size: size of rendered image as a tuple
    :return: filepath of generated image
    """
    image_filepath = Html2Image(browser="chrome", custom_flags=FLAGS).screenshot(
        html_str=html, save_as=out, size=size
    )[0]
    print(f"Generated image from html with size {size}. File located at '{image_filepath}'.")
    return image_filepath


def build_html_update_block_from_member(
    num_films_since_last_update: int,
    name: str,
    place: int,
    num_films_watched: int,
    watchtime: int,
    films_watched_since_last_update,
    show_last_update: bool = True,
    show_watchtime: bool = False,
):
    # html str w/ current score, num of films watched since last update
    html_member = ""
    # html str w/ member's films watched since last update
    html_update = ""
    # html str w/ member's films watched since last update
    html_films = ""
    # set number of films watched since last update if >0 and if watchtime should be shown
    html_films_since_last_update = (
        f"(+{num_films_since_last_update})"
        if num_films_since_last_update > 0 and show_last_update
        else ""
    )
    # format member section of standings template to add member
    html_member += build_html_standings_member_block(
        place=map_place(place),
        name=name,
        num_films_watched=num_films_watched,
        hours_class="hidden" if not show_watchtime else "",
        hours_watched=f"{watchtime / 60:.1f}hrs",
        films_since_last_update=html_films_since_last_update,
    )
    # skip adding member, films to update section if no films in this update
    if num_films_since_last_update < 1 or not show_last_update:
        return html_member, html_update
    # add films to update section's films
    for film in films_watched_since_last_update:
        # format film update template to add films
        html_films += build_html_standings_update_films_block(
            poster=film.poster_url,
            rating=film.rating,
        )
    # add this member to update section of standings template
    html_update += build_html_standings_update_block(name=name, films=html_films)
    return html_member, html_update


def build_html_standings_member_block(
    place: str,
    name: str,
    num_films_watched: str,
    hours_class: str,
    hours_watched: str,
    films_since_last_update: str,
) -> str:
    return constants.HTML_STANDINGS_MEMBER.format(
        place=place,
        name=name,
        num_films_watched=num_films_watched,
        hours_class=hours_class,
        hours_watched=hours_watched,
        films_since_last_update=films_since_last_update,
    )


def build_html_standings_update_block(name: str, films: str) -> str:
    return constants.HTML_STANDINGS_UPDATE.format(
        name=name,
        films=films,
    )


def build_html_standings_update_films_block(poster: str, rating: str) -> str:
    return constants.HTML_STANDINGS_UPDATE_FILMS.format(
        poster=poster,
        rating=rating,
    )


def build_html_standings_block(
    members: str,
    updates: str,
    title: str,
    title_class: str = "",
    members_class: str = "",
    show_update: bool = True,
):
    return constants.HTML_STANDINGS_TEMPLATE.format(
        head=constants.HTML_HEAD,
        title=title,
        members=members,
        updates=updates,
        updates_head_class="" if show_update else "hidden",
        updates_head="Since Last Update" if show_update else "",
        updates_class="films" if show_update else "hidden",
        title_class=title_class,
        members_class=members_class,
        hr_class="films" if show_update else "hidden",
    )


def build_html_avg_watchtimes_block(
    members: str,
):
    return constants.HTML_STANDINGS_TEMPLATE.format(
        head=constants.HTML_HEAD,
        title="Average Watchtimes",
        members=members,
        updates="",
        updates_head_class="hidden",
        updates_head="",
        updates_class="hidden",
        title_class="",
        members_class="",
        hr_class="hidden",
    )


def build_html_avg_watchtime_block_from_member(
    place: int,
    name: str,
    watchtime: int,
    num_films_watched: int,
) -> str:
    # html str w/ current score, num of films watched since last update
    html_member = ""
    # format member section of standings template to add member
    html_member += build_html_standings_member_block(
        place=map_place(place),
        name=name,
        num_films_watched="",
        hours_class="",
        hours_watched=f"{watchtime / 60 / num_films_watched:.2f}hrs",
        films_since_last_update="",
    )
    return html_member


def build_html_unique_films_block_from_member(name: str, place: int, num_unique_films: int) -> str:
    # html str w/ current score, num of films watched since last update
    html_member = ""
    # format member section of standings template to add member
    html_member += build_html_standings_member_block(
        place=map_place(place),
        name=name,
        num_films_watched=num_unique_films,
        hours_class="",
        hours_watched="",
        films_since_last_update="",
    )
    return html_member


def build_html_unique_films_block(
    members: str,
):
    return constants.HTML_STANDINGS_TEMPLATE.format(
        head=constants.HTML_HEAD,
        title="Unique Films",
        members=members,
        updates="",
        updates_head_class="hidden",
        updates_head="",
        updates_class="hidden",
        title_class="",
        members_class="",
        hr_class="hidden",
    )
