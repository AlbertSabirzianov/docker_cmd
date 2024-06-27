import functools

from .constants import ICON_PATH, HELP_TEXT_PATH


@functools.lru_cache
def get_image() -> str:
    with open(ICON_PATH, "r") as file:
        return file.read()


@functools.lru_cache
def get_help_text() -> str:
    with open(HELP_TEXT_PATH, "r") as file:
        return file.read()
