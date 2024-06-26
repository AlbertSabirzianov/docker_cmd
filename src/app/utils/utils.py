import curses
import functools
from typing import TYPE_CHECKING

from .constants import ICON_PATH


@functools.lru_cache
def get_image() -> str:
    with open(ICON_PATH, "r") as file:
        return file.read()


def put_icon_on_screen(stdscr):
    if TYPE_CHECKING:
        stdscr = curses.initscr()
    stdscr.addstr(get_image())
