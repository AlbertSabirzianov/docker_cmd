import curses

from app.utils.enams import Colors
from app.utils.constants import INVISIBLE
from app.viewer.viewer import Viewer


def main(stdscr: curses.window):
    """
    The main function for running the Docker images and containers viewer.

    Parameters:
    - stdscr: A curses.window object representing the terminal window.
    """

    # set colors
    curses.start_color()
    curses.curs_set(INVISIBLE)
    curses.init_pair(Colors.WHITE_ON_BLUE, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(Colors.WHITE_ON_BLACK, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(Colors.WHITE_ON_YELLOW, curses.COLOR_WHITE, curses.COLOR_YELLOW)

    viewer = Viewer(stdscr)
    viewer.run()


if __name__ == "__main__":
    curses.wrapper(main)
