import curses
from typing import TYPE_CHECKING

from app.docker_communicator.docker_comunicator import docker_communicator
from src.app.utils.utils import put_help_text_on_screen


def main(stdscr):

    if TYPE_CHECKING:
        stdscr = curses.initscr()

    while True:
        try:
            stdscr.clear()
            stdscr.addstr(docker_communicator.check_version())
            stdscr.refresh()
            stdscr.getch()

            stdscr.clear()
            stdscr.addstr("CONTAINERS\n")
            stdscr.addstr(docker_communicator.containers())
            stdscr.refresh()
            stdscr.getch()

            stdscr.clear()
            stdscr.addstr("IMAGES\n")
            stdscr.addstr(docker_communicator.images())
            stdscr.refresh()
            stdscr.getch()
        except Exception:
            put_help_text_on_screen(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
