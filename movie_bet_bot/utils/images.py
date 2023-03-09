from typing import Tuple

from html2image import Html2Image


def html_to_image(html: str, out: str = None, size: Tuple[int] = (480, 800)) -> str:
    """
    Create image from html.

    :param html: HTML to render as an image
    :param out: save location of image
    :size: size of rendered image as a tuple
    :return: filepath of generated image
    """
    return Html2Image().screenshot(html_str=html, save_as=out, size=size)[0]
