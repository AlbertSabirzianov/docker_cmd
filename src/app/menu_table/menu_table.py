import curses
from typing import TYPE_CHECKING

from ..utils.enams import MenuChoice, Colors


class MenuTable:

    def __init__(self):
        self.choice: int = MenuChoice.IMAGES

    def is_images(self):
        return self.choice == MenuChoice.IMAGES

    def change_choice(self):
        if self.is_images():
            self.choice = MenuChoice.CONTAINERS
        else:
            self.choice = MenuChoice.IMAGES

    def put_table_on_screen(self, stdscr):
        if TYPE_CHECKING:
            stdscr = curses.initscr()
        _, width = stdscr.getmaxyx()
        center = width // 2

        left_color_number = Colors.WHITE_ON_BLUE if self.is_images() else Colors.WHITE_ON_BLACK
        right_color_number = Colors.WHITE_ON_BLACK if self.is_images() else Colors.WHITE_ON_BLUE

        stdscr.addstr(0, 0, "+" + "-" * (center - 1), curses.color_pair(left_color_number))
        stdscr.addstr(0, center, "+" + "-" * (width - 1), curses.color_pair(right_color_number))
        stdscr.addstr("\n")
        stdscr.addstr(1, 0, "Images" + " " * abs(center - 6), curses.color_pair(left_color_number))
        stdscr.addstr(1, center, "Containers" + " " * abs(center - 10), curses.color_pair(right_color_number))
        stdscr.addstr("\n")


menu_table = MenuTable()

