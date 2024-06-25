import curses
from typing import TYPE_CHECKING


HELP_TEXT_PATH = "images/docker_help_text.txt"


def put_help_text_on_screen(stdscr):

    if TYPE_CHECKING:
        stdscr = curses.initscr()
    stdscr.clear()
    with open(HELP_TEXT_PATH, "r") as file:
        stdscr.addstr(file.read())
    stdscr.refresh()
    stdscr.getch()
