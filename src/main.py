import curses
from typing import TYPE_CHECKING

from app.docker_communicator.docker_comunicator import docker_communicator
from app.utils.utils import put_help_text_on_screen
from app.menu_table.menu_table import menu_table


KEY_EXIT = ord('q')
INVISIBLE = 0


def main(stdscr):
    curses.start_color()
    curses.curs_set(INVISIBLE)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    if TYPE_CHECKING:
        stdscr = curses.initscr()

    while True:
        stdscr.clear()
        menu_table.put_table_on_screen(stdscr)
        stdscr.refresh()
        char = stdscr.getch()
        if char == KEY_EXIT:
            break
        if char in (curses.KEY_RIGHT, curses.KEY_LEFT):
            menu_table.change_choice()

if __name__ == "__main__":
    curses.wrapper(main)
