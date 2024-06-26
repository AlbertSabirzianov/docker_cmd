import functools

from .constants import ICON_PATH


@functools.lru_cache
def get_image() -> str:
    with open(ICON_PATH, "r") as file:
        return file.read()

