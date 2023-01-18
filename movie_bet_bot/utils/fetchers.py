import urllib.request as urllib
from bs4 import BeautifulSoup


async def fetch_page_body_from_url(url: str) -> BeautifulSoup:
    req = urllib.Request(
        url=url,
        data=None,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    try:
        page = urllib.urlopen(req)
    except:
        print(f"Could not open '{url}'.")
        return ""
    return BeautifulSoup(page.read(), "html.parser")
