import curses
from enum import Enum
from typing import TYPE_CHECKING


class MenuChoice(int, Enum):
    IMAGES = 1
    CONTAINERS = 0


class MenuTable:

    def __init__(self):
        self.choice: int = MenuChoice.IMAGES

    def change_choice(self):
        if bool(self.choice):
            self.choice = MenuChoice.CONTAINERS
        else:
            self.choice = MenuChoice.IMAGES

    def put_table_on_screen(self, stdscr):
        if TYPE_CHECKING:
            stdscr = curses.initscr()
        height, width = stdscr.getmaxyx()
        center = width // 2

        left_color_number = 1 if bool(self.choice) else 2
        right_color_number = 2 if bool(self.choice) else 1

        stdscr.addstr(0, 0, "+" + "-" * (center - 1), curses.color_pair(left_color_number))
        stdscr.addstr(0, center, "+" + "-" * (width - 1), curses.color_pair(right_color_number))
        stdscr.addstr("\n")
        stdscr.addstr(1, 0, "Images" + " " * abs(center - 6), curses.color_pair(left_color_number))
        stdscr.addstr(1, center, "Containers" + " " * abs(center - 10), curses.color_pair(right_color_number))
        stdscr.addstr("\n")


menu_table = MenuTable()

