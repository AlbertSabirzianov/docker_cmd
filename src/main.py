import curses
from typing import TYPE_CHECKING

from app.utils.enams import Colors
from app.utils.constants import INVISIBLE
from app.viewer.viewer import Viewer


def main(stdscr):

    # set colors
    curses.start_color()
    curses.curs_set(INVISIBLE)
    curses.init_pair(Colors.WHITE_ON_BLUE, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(Colors.WHITE_ON_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(Colors.WHITE_ON_YELLOW, curses.COLOR_WHITE, curses.COLOR_YELLOW)

    if TYPE_CHECKING:
        stdscr = curses.initscr()

    viewer = Viewer(stdscr)
    viewer.run()


if __name__ == "__main__":
    curses.wrapper(main)
