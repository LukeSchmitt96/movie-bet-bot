import urllib.request as urllib
from urllib.error import URLError

from bs4 import BeautifulSoup

from movie_bet_bot.models.logger import print


async def fetch_page_body_from_url(url: str) -> BeautifulSoup:
    """Get page from a URL.

    :param url: URL of the page to fetch
    :return: BeautifulSoup of page
    """
    req = urllib.Request(
        url=url,
        data=None,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    try:
        page = urllib.urlopen(req)
    except URLError as e:
        print(f"Could not open '{url}': ", e)
        return ""
    return BeautifulSoup(page.read(), "html.parser")
