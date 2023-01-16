from typing import List, Tuple
from html2image import Html2Image


def html_to_image(
    html: str, out: str = None, size: Tuple[int] = (480, 800)
) -> List[str]:
    return Html2Image().screenshot(html_str=html, save_as=out, size=size)
