from typing import Set

import urllib.request as urllib
from bs4 import BeautifulSoup


async def fetch_page_body_from_url(url: str) -> BeautifulSoup:
    try:
        page = urllib.urlopen(url)
    except:
        print(f"Could not open '{url}'.")
        return ''
    return BeautifulSoup(page.read(), 'html.parser')
